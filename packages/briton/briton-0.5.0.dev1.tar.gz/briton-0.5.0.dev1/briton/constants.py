from briton.tool_parsers import (
    Hermes2ProToolParser,
    Llama3JsonToolParser,
    MistralToolParser,
)

OPENAI_NON_COMPATIBLE_TAG = "force-legacy-api-non-openai-compatible"
OPENAI_COMPATIBLE_TAG = "openai-compatible"
DEFAULT_BRITON_PORT = 50051
DEFAULT_TP_COUNT = 1

# Directory where huggingface config.json files are uploaded by engine-builder.
# identical to engine-builder config.json
TOKENIZATION_DIR = "tokenization"


TOOL_CALL_PARSERS = {
    "llama": Llama3JsonToolParser,
    "mistral": MistralToolParser,
    "palmyra": Hermes2ProToolParser,
    "qwen": Hermes2ProToolParser,
}


MODEL_INPUT_TO_BRITON_FIELD = {
    "max_tokens": "request_output_len",
    "beam_width": "beam_width",
    "repetition_penalty": "repetition_penalty",
    "presence_penalty": "presence_penalty",
    "temperature": "temperature",
    "length_penalty": "len_penalty",
    "end_id": "end_id",
    "pad_id": "pad_id",
    "runtime_top_k": "runtime_top_k",
    "runtime_top_p": "runtime_top_p",
    "random_seed": "random_seed",
    "stop_words": "stop_words",
    "bad_words": "bad_words",
}

UINT32_MAX = 2**32 - 1

BRITON_DEFAULT_MAX_TOKENS = 50

TRT_CONFIG_FILENAME = "config.json"
