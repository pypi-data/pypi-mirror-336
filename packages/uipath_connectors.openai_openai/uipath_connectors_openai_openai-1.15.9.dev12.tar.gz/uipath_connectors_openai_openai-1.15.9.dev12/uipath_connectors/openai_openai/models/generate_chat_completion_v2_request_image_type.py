from enum import Enum


class GenerateChatCompletionV2RequestImageType(str, Enum):
    IMAGE_FILE = "Image file"
    IMAGE_URL = "Image URL"

    def __str__(self) -> str:
        return str(self.value)
