from .v2chatcompletion import (
    generate_chat_completion_v2 as _generate_chat_completion_v2,
    generate_chat_completion_v2_async as _generate_chat_completion_v2_async,
)
from ..models.default_error import DefaultError
from ..models.generate_chat_completion_v2_body import GenerateChatCompletionV2Body
from ..models.generate_chat_completion_v2_request import GenerateChatCompletionV2Request
from ..models.generate_chat_completion_v2_response import (
    GenerateChatCompletionV2Response,
)
from typing import cast
from .generate_text_completion import (
    generate_text_completion as _generate_text_completion,
    generate_text_completion_async as _generate_text_completion_async,
)
from ..models.generate_text_completion_request import GenerateTextCompletionRequest
from ..models.generate_text_completion_response import GenerateTextCompletionResponse

from pydantic import Field
from typing import Any, Optional, Union

from ..client import Client
import httpx


class OpenaiOpenai:
    def __init__(self, *, instance_id: str, client: httpx.Client):
        base_url = str(client.base_url).rstrip("/")
        new_headers = {
            k: v for k, v in client.headers.items() if k not in ["content-type"]
        }
        new_client = httpx.Client(
            base_url=base_url + f"/elements_/v3/element/instances/{instance_id}",
            headers=new_headers,
            timeout=100,
        )
        new_client_async = httpx.AsyncClient(
            base_url=base_url + f"/elements_/v3/element/instances/{instance_id}",
            headers=new_headers,
            timeout=100,
        )
        self.client = (
            Client(
                base_url="",  # this will be overridden by the base_url in the Client constructor
            )
            .set_httpx_client(new_client)
            .set_async_httpx_client(new_client_async)
        )

    def generate_chat_completion_v2(
        self,
        *,
        body: GenerateChatCompletionV2Body,
    ) -> Optional[Union[DefaultError, GenerateChatCompletionV2Response]]:
        return _generate_chat_completion_v2(
            client=self.client,
            body=body,
        )

    async def generate_chat_completion_v2_async(
        self,
        *,
        body: GenerateChatCompletionV2Body,
    ) -> Optional[Union[DefaultError, GenerateChatCompletionV2Response]]:
        return await _generate_chat_completion_v2_async(
            client=self.client,
            body=body,
        )

    def generate_text_completion(
        self,
        *,
        body: GenerateTextCompletionRequest,
    ) -> Optional[Union[DefaultError, GenerateTextCompletionResponse]]:
        return _generate_text_completion(
            client=self.client,
            body=body,
        )

    async def generate_text_completion_async(
        self,
        *,
        body: GenerateTextCompletionRequest,
    ) -> Optional[Union[DefaultError, GenerateTextCompletionResponse]]:
        return await _generate_text_completion_async(
            client=self.client,
            body=body,
        )
