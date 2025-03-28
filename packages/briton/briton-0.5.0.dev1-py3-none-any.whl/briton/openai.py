import json
import logging
import time
from typing import AsyncGenerator, Callable, List, Literal, Optional, Tuple

import openai.types.chat.chat_completion as chat_completion
import openai.types.chat.chat_completion_chunk as chat_completion_chunk
from openai.types.chat import ChatCompletion, ChatCompletionChunk
from openai.types.chat.chat_completion_chunk import ChoiceDelta
from openai.types.chat.chat_completion_message import ChatCompletionMessage
from openai.types.chat.chat_completion_token_logprob import (
    ChatCompletionTokenLogprob,
    TopLogprob,
)
from openai.types.completion import Completion
from openai.types.completion_choice import CompletionChoice
from openai.types.completion_usage import CompletionUsage
from transformers import PreTrainedTokenizerFast

from briton.async_util import interleave_generators
from briton.proto import FinishReason, InferenceAnswerPart
from briton.tool_parsers import ToolParser

logger = logging.getLogger(__name__)


def _finish_reason_from_text(
    text: str, eos_token: Optional[str] = None, stop_words: Optional[List[str]] = None
) -> Literal["stop", "length"]:
    if eos_token and text.endswith(eos_token):
        return "stop"
    if stop_words and text.endswith(tuple(stop_words)):
        return "stop"
    return "length"


def _finish_reason_from_inference_answer_part(
    inference_answer_part: InferenceAnswerPart,
    eos_token: Optional[str] = None,
    stop_words: Optional[List[str]] = None,
) -> Literal["stop", "length"]:
    if inference_answer_part.finish_reason != FinishReason.NOT_FINISHED:
        return "length" if inference_answer_part.finish_reason == FinishReason.LENGTH else "stop"
    else:
        return _finish_reason_from_text(inference_answer_part.output_text, eos_token, stop_words)


def remove_suffix_from_text(
    text: str,
    eos_token: Optional[str] = None,
    stop_words: Optional[List[str]] = None,
    skip_special_tokens: Optional[List[str]] = None,
) -> str:
    if eos_token is not None and text.endswith(eos_token):
        return text.removesuffix(eos_token)
    if stop_words is not None:
        for stop_word in stop_words:
            if text.endswith(stop_word):
                return text.removesuffix(stop_word)
    # HACK (bdubayah): this could end up being very expensive.
    if skip_special_tokens is not None:
        for special_token in skip_special_tokens:
            text = text.replace(special_token, "")
    return text


def _create_choice(
    index: int,
    inference_answer: InferenceAnswerPart,
    tokenizer: PreTrainedTokenizerFast,
    eos_token: Optional[str],
    tool_parser_class: Optional[type[ToolParser]],
    stop_words: Optional[List[str]],
    skip_special_tokens: Optional[List[str]],
    top_logprobs: Optional[int],
    is_chat_completion: bool,
) -> chat_completion.Choice | CompletionChoice:
    finish_reason = _finish_reason_from_inference_answer_part(
        inference_answer, eos_token, stop_words
    )
    content = remove_suffix_from_text(
        text=inference_answer.output_text,
        eos_token=eos_token,
        stop_words=stop_words,
        skip_special_tokens=skip_special_tokens,
    )
    if is_chat_completion:
        tool_calls = None
        if tool_parser_class is not None:
            tool_parser = tool_parser_class(tokenizer)
            maybe_tool_calls = tool_parser.extract_tool_calls(content)
            if maybe_tool_calls.tools_called:
                finish_reason = "tool_calls"
                content = maybe_tool_calls.content
                tool_calls = maybe_tool_calls.tool_calls
        message = ChatCompletionMessage(content=content, role="assistant", tool_calls=tool_calls)
        logprobs_content = _create_choice_log_probs(inference_answer, top_logprobs, tokenizer)
        logprobs = (
            chat_completion.ChoiceLogprobs(content=logprobs_content)
            if logprobs_content is not None
            else None
        )
        return chat_completion.Choice(
            finish_reason=finish_reason, index=index, message=message, logprobs=logprobs
        )
    else:
        if content is None:
            content = ""
        # TODO(@bdubayah): add logprobs to completions
        return CompletionChoice(finish_reason=finish_reason, index=index, text=content)


def create_completion(
    req_id: str,
    model: str,
    inference_answers: List[InferenceAnswerPart],
    tokenizer: PreTrainedTokenizerFast,
    eos_token: Optional[str] = None,
    tool_parser_class: Optional[type[ToolParser]] = None,
    prompt_tokens: Optional[int] = None,
    completion_tokens: Optional[int] = None,
    stop_words: Optional[List[str]] = None,
    skip_special_tokens: Optional[List[str]] = None,
    top_logprobs: Optional[int] = None,
    is_chat_completion: bool = False,
) -> ChatCompletion | Completion:
    created = int(time.time())
    choices = []
    for i, inference_answer in enumerate(inference_answers):
        choice = _create_choice(
            index=i,
            inference_answer=inference_answer,
            tokenizer=tokenizer,
            eos_token=eos_token,
            tool_parser_class=tool_parser_class,
            stop_words=stop_words,
            skip_special_tokens=skip_special_tokens,
            top_logprobs=top_logprobs,
            is_chat_completion=is_chat_completion,
        )
        choices.append(choice)
    usage = None
    if prompt_tokens is not None and completion_tokens is not None:
        usage = CompletionUsage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
        )
    if is_chat_completion:
        return ChatCompletion(
            id=req_id,
            choices=choices,
            created=created,
            model=model,
            object="chat.completion",
            usage=usage,
        )
    else:
        return Completion(
            id=req_id,
            choices=choices,
            created=created,
            model=model,
            object="text_completion",
            usage=usage,
        )


def _make_sse_chunk(chunk: ChatCompletionChunk | Completion) -> str:
    return f"data: {chunk.model_dump_json()}\n\n"


def _get_token_and_bytes(
    token_id: int, tokenizer: PreTrainedTokenizerFast
) -> Tuple[str, List[int]]:
    token = tokenizer.convert_ids_to_tokens(token_id)
    assert isinstance(token, str)
    token_bytes = list(token.encode("utf-8"))
    return token, token_bytes


def _create_choice_log_probs(
    inference_answer_part: InferenceAnswerPart,
    top_logprobs: Optional[int],
    tokenizer: PreTrainedTokenizerFast,
) -> Optional[List[ChatCompletionTokenLogprob]]:
    num_top_logprobs = len(inference_answer_part.top_logprobs)
    num_output_ids = len(inference_answer_part.output_ids)
    if num_top_logprobs == 0 or num_output_ids != num_top_logprobs:
        return None
    content: List[ChatCompletionTokenLogprob] = []
    for token_id, top_logprobs_proto in zip(
        inference_answer_part.output_ids, inference_answer_part.top_logprobs
    ):
        top_logprobs_list = []
        if top_logprobs is not None and top_logprobs > 0:
            for child_token_id, child_logprob in top_logprobs_proto.logprobs.items():
                child_token, child_token_bytes = _get_token_and_bytes(child_token_id, tokenizer)
                top_logprob = TopLogprob(
                    token=child_token, bytes=child_token_bytes, logprob=child_logprob
                )
                top_logprobs_list.append(top_logprob)
        token, token_bytes = _get_token_and_bytes(token_id, tokenizer)
        token_logprob = ChatCompletionTokenLogprob(
            token=token,
            logprob=top_logprobs_proto.logprob,
            bytes=token_bytes,
            top_logprobs=top_logprobs_list,
        )
        content.append(token_logprob)
    return content


def _create_completion_chunk(
    id: str,
    created: int,
    index: int,
    model: str,
    is_chat_completion: bool,
    choice_delta: chat_completion_chunk.ChoiceDelta,
    finish_reason: Optional[
        Literal["stop", "length", "tool_calls", "content_filter", "function_call"]
    ] = None,
    logprobs: Optional[chat_completion_chunk.ChoiceLogprobs] = None,
) -> ChatCompletionChunk | Completion:
    if is_chat_completion:
        choice = chat_completion_chunk.Choice(
            index=index, delta=choice_delta, finish_reason=finish_reason, logprobs=logprobs
        )
        return ChatCompletionChunk(
            id=id,
            choices=[choice],
            created=created,
            model=model,
            object="chat.completion.chunk",
        )
    else:
        text = choice_delta.content
        if text is None:
            text = ""
        if finish_reason is None:
            finish_reason = "length"
        choice = CompletionChoice(index=index, text=text, finish_reason=finish_reason)
        return Completion(
            id=id,
            choices=[choice],
            created=created,
            model=model,
            object="text_completion",
        )


async def _create_completion_chunks(
    created: int,
    req_id: str,
    index: int,
    model: str,
    response_stream: AsyncGenerator[InferenceAnswerPart, None],
    tokenizer: PreTrainedTokenizerFast,
    eos_token: Optional[str],
    tool_parser_class: Optional[type[ToolParser]],
    stop_words: Optional[List[str]],
    skip_special_tokens: Optional[List[str]],
    top_logprobs: Optional[int],
    is_chat_completion: bool,
) -> AsyncGenerator[ChatCompletionChunk | Completion, None]:
    previous_text = ""
    previous_token_ids = []
    tool_parser = None
    if tool_parser_class is not None:
        tool_parser = tool_parser_class(tokenizer)

    start_chunk = _create_completion_chunk(
        id=req_id,
        created=created,
        index=index,
        model=model,
        choice_delta=ChoiceDelta(role="assistant"),
        is_chat_completion=is_chat_completion,
    )

    is_first_iter = True
    inference_answer_part = None
    async for inference_answer_part in response_stream:
        if is_first_iter:
            is_first_iter = False
            yield start_chunk

        content = remove_suffix_from_text(
            text=inference_answer_part.output_text,
            eos_token=eos_token,
            stop_words=stop_words,
            skip_special_tokens=skip_special_tokens,
        )

        # Don't send empty chunks
        if len(content) == 0:
            continue

        if tool_parser is not None:
            current_text = previous_text + content
            current_token_ids = previous_token_ids + list(inference_answer_part.output_ids)
            choice_delta = tool_parser.extract_tool_calls_streaming(
                previous_text=previous_text,
                current_text=current_text,
                delta_text=content,
                previous_token_ids=previous_token_ids,
                current_token_ids=current_token_ids,
                delta_token_ids=inference_answer_part.output_ids,
            )
            previous_text = current_text
            previous_token_ids = current_token_ids
        else:
            choice_delta = ChoiceDelta(content=content)

        if choice_delta is None:
            continue

        logprobs_content = _create_choice_log_probs(inference_answer_part, top_logprobs, tokenizer)
        logprobs = (
            chat_completion_chunk.ChoiceLogprobs(content=logprobs_content)
            if logprobs_content is not None
            else None
        )
        yield _create_completion_chunk(
            id=req_id,
            created=created,
            index=index,
            model=model,
            choice_delta=choice_delta,
            logprobs=logprobs,
            is_chat_completion=is_chat_completion,
        )

    tools_called = tool_parser and len(tool_parser.prev_tool_call_arr) > 0
    if tools_called:
        finish_reason = "tool_calls"
    else:
        if inference_answer_part is None:
            finish_reason = "length"
        else:
            finish_reason = _finish_reason_from_inference_answer_part(
                inference_answer_part, eos_token, stop_words
            )

    yield _create_completion_chunk(
        id=req_id,
        created=created,
        index=index,
        model=model,
        choice_delta=ChoiceDelta(),
        finish_reason=finish_reason,
        is_chat_completion=is_chat_completion,
    )


async def create_completion_chunks(
    req_id: str,
    model: str,
    response_streams: List[AsyncGenerator[InferenceAnswerPart, None]],
    tokenizer: PreTrainedTokenizerFast,
    eos_token: Optional[str] = None,
    tool_parser_class: Optional[type[ToolParser]] = None,
    prompt_tokens: Optional[int] = None,
    completion_tokens_fn: Optional[Callable[[], int]] = None,
    stop_words: Optional[List[str]] = None,
    skip_special_tokens: Optional[List[str]] = None,
    top_logprobs: Optional[int] = None,
    is_chat_completion: bool = False,
) -> AsyncGenerator[str, None]:
    created = int(time.time())

    chunk_generators = [
        _create_completion_chunks(
            created=created,
            req_id=req_id,
            index=i,
            model=model,
            response_stream=response_stream,
            tokenizer=tokenizer,
            eos_token=eos_token,
            tool_parser_class=tool_parser_class,
            stop_words=stop_words,
            skip_special_tokens=skip_special_tokens,
            top_logprobs=top_logprobs,
            is_chat_completion=is_chat_completion,
        )
        for i, response_stream in enumerate(response_streams)
    ]
    async for chunk in interleave_generators(*chunk_generators):
        yield _make_sse_chunk(chunk)

    if prompt_tokens is not None and completion_tokens_fn is not None:
        completion_tokens = completion_tokens_fn()
        usage = CompletionUsage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
        )
        if is_chat_completion:
            usage_chunk = ChatCompletionChunk(
                id=req_id,
                choices=[],
                created=created,
                model=model,
                object="chat.completion.chunk",
                usage=usage,
            )
        else:
            usage_chunk = Completion(
                id=req_id,
                choices=[],
                created=created,
                model=model,
                object="text_completion",
                usage=usage,
            )
        yield _make_sse_chunk(usage_chunk)

    yield "data: [DONE]\n\n"
