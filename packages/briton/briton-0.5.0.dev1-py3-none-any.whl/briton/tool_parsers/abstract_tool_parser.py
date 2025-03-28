import uuid
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Sequence

from openai.types.chat.chat_completion_chunk import ChoiceDelta
from openai.types.chat.chat_completion_message_tool_call import (
    ChatCompletionMessageToolCall,
)
from pydantic import BaseModel
from transformers import PreTrainedTokenizerFast


class ExtractedToolCallInformation(BaseModel):
    tools_called: bool
    tool_calls: List[ChatCompletionMessageToolCall]
    content: Optional[str] = None


def random_uuid() -> str:
    return str(uuid.uuid4().hex)


class ToolParser(ABC):
    def __init__(self, tokenizer: PreTrainedTokenizerFast):
        self.prev_tool_call_arr: List[Dict] = []
        self.current_tool_id: int = -1
        self.current_tool_name_sent: bool = False
        self.streamed_args_for_tool: List[str] = []
        self.model_tokenizer = tokenizer

    @property
    def vocab(self) -> Dict[str, int]:
        return self.model_tokenizer.vocab

    @abstractmethod
    def extract_tool_calls(self, model_output: str) -> ExtractedToolCallInformation: ...

    @abstractmethod
    def extract_tool_calls_streaming(
        self,
        previous_text: str,
        current_text: str,
        delta_text: str,
        previous_token_ids: Sequence[int],
        current_token_ids: Sequence[int],
        delta_token_ids: Sequence[int],
    ) -> Optional[ChoiceDelta]: ...
