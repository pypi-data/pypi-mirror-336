from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.generate_chat_completion_v2_request_image_type import (
    GenerateChatCompletionV2RequestImageType,
)
from ..models.generate_chat_completion_v2_request_model import (
    GenerateChatCompletionV2RequestModel,
)


class GenerateChatCompletionV2Request(BaseModel):
    """
    Attributes:
        model (GenerateChatCompletionV2RequestModel): The large language model (LLM) to use for the chat completion.
                Defaults to gpt-4o. Default: GenerateChatCompletionV2RequestModel.GPT_4_O. Example: gpt-4o.
        prompt (str): The input to use for the chat completion request. Example: Write an email to a new sales lead.
        frequency_penalty (Optional[float]): Number between -2.0 and 2.0. Positive values penalize new tokens based on
                their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.
                Defaults to 0. Default: 0.0. Example: 0.
        image_type (Optional[GenerateChatCompletionV2RequestImageType]): The type of image to send along with a message
                if image analysis is needed.
        image_url (Optional[str]): The image URL to send along with a message if image analysis is needed.  Note: this
                will only work with the GPT-4-Turbo and GPT-4o model
        instruction (Optional[str]): Instructions guide the AI to respond in a way that matches your intent. Defaults to
                null. Example: Write in a friendly tone or The assistant is helpful.
        max_tokens (Optional[int]): The maximum number of tokens allowed for the prompt and generated answer. Fewer
                tokens are less expensive. Defaults to 3840. Default: 1920. Example: 3840.0.
        n (Optional[int]): A number of at least 1.  This determines how many completion choices the AI will return.
                Defaults to 1. Default: 1. Example: 1.0.
        presence_penalty (Optional[float]): Number between -2.0 and 2.0. Positive values penalize new tokens based on
                whether they appear in the text so far, increasing the model's likelihood to talk about new topics. Defaults to
                0. Default: 0.0. Example: 0.
        stop (Optional[str]): Up to 4 sequences where the API will stop generating further tokens. The returned text
                will not contain the stop sequence. Defaults to null.
        temperature (Optional[float]): ⌘ ⌥ K
                A number between 0 and 2.  Higher values like 0.8 will make the output more random, while lower values like 0.2
                will make it more focused and deterministic. Defaults to 1. Default: 1.0. Example: 1.
        top_p (Optional[float]): A number between 0 and 1.  The lower the number, the fewer tokens are considered.
                Defaults to 1. Default: 1.0. Example: 1.0.
        user (Optional[str]): A unique identifier representing your end-user, which can help OpenAI to monitor and
                detect abuse. Defaults to null.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    prompt: str = Field(alias="prompt")
    model: "GenerateChatCompletionV2RequestModel" = Field(
        alias="model", default=GenerateChatCompletionV2RequestModel.GPT_4_O
    )
    frequency_penalty: Optional[float] = Field(alias="frequency_penalty", default=0.0)
    image_type: Optional["GenerateChatCompletionV2RequestImageType"] = Field(
        alias="image_type", default=None
    )
    image_url: Optional[str] = Field(alias="image_url", default=None)
    instruction: Optional[str] = Field(alias="instruction", default=None)
    max_tokens: Optional[int] = Field(alias="max_tokens", default=1920)
    n: Optional[int] = Field(alias="n", default=1)
    presence_penalty: Optional[float] = Field(alias="presence_penalty", default=0.0)
    stop: Optional[str] = Field(alias="stop", default=None)
    temperature: Optional[float] = Field(alias="temperature", default=1.0)
    top_p: Optional[float] = Field(alias="top_p", default=1.0)
    user: Optional[str] = Field(alias="user", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["GenerateChatCompletionV2Request"], src_dict: Dict[str, Any]
    ):
        return cls.model_validate(src_dict)

    @property
    def additional_keys(self) -> list[str]:
        base_fields = self.model_fields.keys()
        return [k for k in self.__dict__ if k not in base_fields]

    def __getitem__(self, key: str) -> Any:
        if key in self.__dict__:
            return self.__dict__[key]
        raise KeyError(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self.__dict__[key] = value

    def __delitem__(self, key: str) -> None:
        if key in self.__dict__:
            del self.__dict__[key]
        else:
            raise KeyError(key)

    def __contains__(self, key: str) -> bool:
        return key in self.__dict__
