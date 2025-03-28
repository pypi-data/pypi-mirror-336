import json
import logging
import re
from random import choices
from string import ascii_letters, digits
from typing import Any, Dict, List, Sequence, Union, cast

import partial_json_parser
from openai.types.chat.chat_completion_chunk import (
    ChoiceDelta,
    ChoiceDeltaToolCall,
    ChoiceDeltaToolCallFunction,
)
from openai.types.chat.chat_completion_message_tool_call import (
    ChatCompletionMessageToolCall,
    Function,
)
from partial_json_parser.core.options import Allow
from transformers import PreTrainedTokenizerFast

from briton.tool_parsers.abstract_tool_parser import (
    ExtractedToolCallInformation,
    ToolParser,
)
from briton.tool_parsers.utils import extract_intermediate_diff

logger = logging.getLogger(__name__)

ALPHANUMERIC = ascii_letters + digits


class MistralToolParser(ToolParser):
    """
    Tool call parser for Mistral 7B Instruct, intended for use with the
    examples/tool_chat_template_mistral.jinja template.
    """

    def __init__(self, tokenizer: PreTrainedTokenizerFast):
        super().__init__(tokenizer)

        # initialize properties used for state when parsing tool calls in
        # streaming mode
        self.prev_tool_call_arr: List[Dict[str, Any]] = []
        self.current_tool_id: int = -1
        self.current_tool_name_sent: bool = False
        self.streamed_args_for_tool: List[str] = (
            []
        )  # map what has been streamed for each tool so far to a list
        self.bot_token = "[TOOL_CALLS]"
        self.bot_token_id = self.vocab.get(self.bot_token)
        self.tool_call_regex = re.compile(r"\[{.*}\]", re.DOTALL)
        if self.bot_token_id is None:
            raise RuntimeError(
                "Mistral Tool Parser could not locate the tool call token in " "the tokenizer!"
            )

    def extract_tool_calls(
        self,
        model_output: str,
    ) -> ExtractedToolCallInformation:
        """
        Extract the tool calls from a complete model response. Requires
        find-and-replacing single quotes with double quotes for JSON parsing,
        make sure your tool call arguments don't ever include quotes!
        """

        # case -- if a tool call token is not present, return a text response
        if self.bot_token not in model_output:
            return ExtractedToolCallInformation(
                tools_called=False, tool_calls=[], content=model_output
            )

        # first remove the BOT token
        tool_content = model_output.replace(self.bot_token, "").strip()

        try:

            # we first try to directly load the json as parsing very nested
            # jsons is difficult
            try:
                function_call_arr = json.loads(tool_content)
            except json.JSONDecodeError:
                # use a regex to find the part corresponding to the tool call.
                # NOTE: This use case should not happen if the model is trained
                # correctly. It's a easy possible fix so it's included, but
                # can be brittle for very complex / highly nested tool calls
                raw_tool_call = self.tool_call_regex.findall(tool_content)[0]
                function_call_arr = json.loads(raw_tool_call)

            # Tool Call
            tool_calls: List[ChatCompletionMessageToolCall] = [
                ChatCompletionMessageToolCall(
                    type="function",
                    function=Function(
                        name=raw_function_call["name"],
                        # function call args are JSON but as a string
                        arguments=json.dumps(raw_function_call["arguments"], ensure_ascii=False),
                    ),
                    id=self._generate_mistral_tool_id(),
                )
                for raw_function_call in function_call_arr
            ]

            # get any content before  the tool call
            content = model_output.split(self.bot_token)[0]
            return ExtractedToolCallInformation(
                tools_called=True,
                tool_calls=tool_calls,
                content=content if len(content) > 0 else None,
            )

        except Exception:
            logger.exception("Error in extracting tool call from response.")
            # return information to just treat the tool call as regular JSON
            return ExtractedToolCallInformation(
                tools_called=False, tool_calls=[], content=tool_content
            )

    def _generate_mistral_tool_id(self) -> str:
        """
        Mistral Tool Call Ids must be alphanumeric with a maximum length of 9.
        """
        return "".join(choices(ALPHANUMERIC, k=9))

    def extract_tool_calls_streaming(
        self,
        previous_text: str,
        current_text: str,
        delta_text: str,
        previous_token_ids: Sequence[int],
        current_token_ids: Sequence[int],
        delta_token_ids: Sequence[int],
    ) -> Union[ChoiceDelta, None]:

        # if the tool call token is not in the tokens generated so far, append
        # output to contents since it's not a tool
        if self.bot_token not in current_text:
            return ChoiceDelta(content=delta_text)

        # if the tool call token ID IS in the tokens generated so far, that
        # means we're parsing as tool calls now

        # handle if we detected the BOT token which means the start of tool
        # calling
        if self.bot_token_id in delta_token_ids and len(delta_token_ids) == 1:
            # if it's the only token, return None, so we don't send a chat
            # completion any don't send a control token
            return None

        # bit mask flags for partial JSON parsing. If the name hasn't been
        # sent yet, don't allow sending
        # an incomplete string since OpenAI only ever (as far as I have
        # seen) allows sending the entire tool/ function name at once.
        flags = Allow.ALL if self.current_tool_name_sent else Allow.ALL & ~Allow.STR
        try:

            # replace BOT token with empty string, and convert single quotes
            # to double to allow parsing as JSON since mistral uses single
            # quotes instead of double for tool calls
            parsable_arr = current_text.split(self.bot_token)[-1]

            # tool calls are generated in an array, so do partial JSON
            # parsing on the entire array
            try:
                tool_call_arr_json = partial_json_parser.loads(parsable_arr, flags)
                # Cast to ensure it's treated as a list of dicts
                tool_call_arr: List[Dict[str, Any]] = cast(List[Dict[str, Any]], tool_call_arr_json)
            except json.JSONDecodeError:
                logger.debug("not enough tokens to parse into JSON yet")
                return None

            # select as the current tool call the one we're on the state at
            current_tool_call: Dict[str, Any] = (
                tool_call_arr[self.current_tool_id] if len(tool_call_arr) > 0 else {}
            )

            # case -- if no tokens have been streamed for the tool, e.g.
            #   only the array brackets, stream nothing
            if len(tool_call_arr) == 0:
                return None

            # case: we are starting a new tool in the array
            #   -> array has > 0 length AND length has moved past cursor
            elif len(tool_call_arr) > 0 and len(tool_call_arr) > self.current_tool_id + 1:

                # if we're moving on to a new call, first make sure we
                # haven't missed anything in the previous one that was
                # auto-generated due to JSON completions, but wasn't
                # streamed to the client yet.
                if self.current_tool_id >= 0:
                    diff: Union[str, None] = current_tool_call.get("arguments")

                    if diff:
                        diff = json.dumps(diff, ensure_ascii=False).replace(
                            self.streamed_args_for_tool[self.current_tool_id], ""
                        )
                        delta = ChoiceDelta(
                            tool_calls=[
                                ChoiceDeltaToolCall(
                                    index=self.current_tool_id,
                                    function=ChoiceDeltaToolCallFunction(arguments=diff),
                                ),
                            ]
                        )
                        self.streamed_args_for_tool[self.current_tool_id] += diff
                    else:
                        delta = None
                else:
                    delta = None
                # re-set stuff pertaining to progress in the current tool
                self.current_tool_id = len(tool_call_arr) - 1
                self.current_tool_name_sent = False
                self.streamed_args_for_tool.append("")
                logger.debug("starting on new tool %d", self.current_tool_id)
                return delta

            # case: update an existing tool - this is handled below

            # if the current tool name hasn't been sent, send if available
            # - otherwise send nothing
            if not self.current_tool_name_sent:
                function_name = current_tool_call.get("name")
                if function_name:
                    delta = ChoiceDelta(
                        tool_calls=[
                            ChoiceDeltaToolCall(
                                index=self.current_tool_id,
                                type="function",
                                id=self._generate_mistral_tool_id(),
                                function=ChoiceDeltaToolCallFunction(name=function_name),
                            ),
                        ]
                    )
                    self.current_tool_name_sent = True
                else:
                    delta = None

            # now we know we're on the same tool call and we're streaming
            # arguments
            else:
                prev_arguments = self.prev_tool_call_arr[self.current_tool_id].get("arguments")
                cur_arguments = current_tool_call.get("arguments")

                if not cur_arguments:
                    delta = None
                elif not prev_arguments:
                    cur_arguments_json = json.dumps(cur_arguments, ensure_ascii=False)
                    arguments_delta = extract_intermediate_diff(cur_arguments_json, "")
                    delta = ChoiceDelta(
                        tool_calls=[
                            ChoiceDeltaToolCall(
                                index=self.current_tool_id,
                                function=ChoiceDeltaToolCallFunction(arguments=arguments_delta),
                            ),
                        ]
                    )
                    self.streamed_args_for_tool[self.current_tool_id] += arguments_delta
                else:
                    arguments_diff = extract_intermediate_diff(
                        json.dumps(cur_arguments, ensure_ascii=False),
                        json.dumps(prev_arguments, ensure_ascii=False),
                    )

                    if arguments_diff:
                        delta = ChoiceDelta(
                            tool_calls=[
                                ChoiceDeltaToolCall(
                                    index=self.current_tool_id,
                                    function=ChoiceDeltaToolCallFunction(arguments=arguments_diff),
                                ),
                            ]
                        )
                        self.streamed_args_for_tool[self.current_tool_id] += arguments_diff
                    else:
                        delta = None

            self.prev_tool_call_arr = tool_call_arr
            return delta

        except Exception:
            logger.exception("Error trying to handle streaming tool call.")
            return None  # do not stream a delta. skip this token ID.
