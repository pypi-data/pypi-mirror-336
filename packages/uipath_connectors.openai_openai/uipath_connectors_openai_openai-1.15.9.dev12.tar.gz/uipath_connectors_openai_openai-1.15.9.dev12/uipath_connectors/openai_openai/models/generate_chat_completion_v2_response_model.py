from enum import Enum


class GenerateChatCompletionV2ResponseModel(str, Enum):
    GPT_35_TURBO = "gpt-3.5-turbo"
    GPT_4 = "gpt-4"
    GPT_4_O = "gpt-4o"
    GPT_4_TURBO = "gpt-4-turbo"

    def __str__(self) -> str:
        return str(self.value)
