from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.generate_text_completion_request_model import (
    GenerateTextCompletionRequestModel,
)


class GenerateTextCompletionRequest(BaseModel):
    """
    Attributes:
        prompt (str): The prompt to use for the text completion(s) generation Default: 'Write an email to a new sales
                lead'. Example: Write an email to a new sales lead.
        best_of (Optional[int]): Generates best_of completions server-side and returns the "best" (the one with the
                highest log probability per token). Results cannot be streamed.

                When used with n, best_of controls the number of candidate completions and n specifies how many to return –
                best_of must be greater than n.

                Note: Because this parameter generates many completions, it can quickly consume your token quota. Use carefully
                and ensure that you have reasonable settings for max_tokens and stop. Defaults to 1 Default: 1. Example: 1.
        echo (Optional[bool]): Echo back the prompt in addition to the completion. Defaults to false. Default: False.
        frequency_penalty (Optional[float]): Number between -2.0 and 2.0. Positive values penalize new tokens based on
                their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.
                Defaults to 0. Default: 0.0. Example: 0.
        logprobs (Optional[int]): Include the log probabilities on the logprobs most likely tokens, as well the chosen
                tokens. For example, if logprobs is 5, the API will return a list of the 5 most likely tokens. The API will
                always return the logprob of the sampled token, so there may be up to logprobs+1 elements in the response.

                The maximum value for logprobs is 5. Defaults to null.
        max_tokens (Optional[int]): The maximum number of tokens allowed for the prompt and generated answer. Fewer
                tokens are less expensive. Most models support a maximum of 4096 tokens, however, some models support only 2048.
                Defaults to 1920. Default: 1920. Example: 1920.
        model (Optional[GenerateTextCompletionRequestModel]): The large language model (LLM) to use for the text
                completion. Defaults to gpt-3.5-turbo-instruct Default:
                GenerateTextCompletionRequestModel.GPT_35_TURBO_INSTRUCT. Example: gpt-3.5-turbo-instruct.
        n (Optional[int]): A number of at least 1.  This determines how many completion choices the AI will return.
                Defaults to 1. Default: 1. Example: 1.0.
        presence_penalty (Optional[float]): Number between -2.0 and 2.0. Positive values penalize new tokens based on
                whether they appear in the text so far, increasing the model's likelihood to talk about new topics. Defaults to
                0. Default: 0.0. Example: 0.
        stop (Optional[str]): Up to 4 sequences where the API will stop generating further tokens. The returned text
                will not contain the stop sequence. Defaults to null.
        stream (Optional[bool]): Whether to stream back partial progress. If set, tokens will be sent as data-only
                server-sent events as they become available, with the stream terminated by a data: [DONE] message. Defaults to
                false. Default: False.
        suffix (Optional[str]): The suffix that comes after a completion of inserted text. Defaults to null.
        temperature (Optional[float]): A number between 0 and 2.  Higher values like 0.8 will make the output more
                random, while lower values like 0.2 will make it more focused and deterministic. Defaults to 1 Default: 1.0.
                Example: 1.0.
        top_p (Optional[float]): A number between 0 and 1.  The lower the number, the fewer tokens are considered.
                Defaults to 1. Default: 1.0. Example: 1.0.
        user (Optional[str]): A unique identifier representing your end-user, which can help OpenAI to monitor and
                detect abuse. Defaults to null.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    prompt: str = Field(alias="prompt", default="Write an email to a new sales lead")
    best_of: Optional[int] = Field(alias="best_of", default=1)
    echo: Optional[bool] = Field(alias="echo", default=False)
    frequency_penalty: Optional[float] = Field(alias="frequency_penalty", default=0.0)
    logprobs: Optional[int] = Field(alias="logprobs", default=None)
    max_tokens: Optional[int] = Field(alias="max_tokens", default=1920)
    model: Optional["GenerateTextCompletionRequestModel"] = Field(
        alias="model", default=GenerateTextCompletionRequestModel.GPT_35_TURBO_INSTRUCT
    )
    n: Optional[int] = Field(alias="n", default=1)
    presence_penalty: Optional[float] = Field(alias="presence_penalty", default=0.0)
    stop: Optional[str] = Field(alias="stop", default=None)
    stream: Optional[bool] = Field(alias="stream", default=False)
    suffix: Optional[str] = Field(alias="suffix", default=None)
    temperature: Optional[float] = Field(alias="temperature", default=1.0)
    top_p: Optional[float] = Field(alias="top_p", default=1.0)
    user: Optional[str] = Field(alias="user", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["GenerateTextCompletionRequest"], src_dict: Dict[str, Any]):
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
