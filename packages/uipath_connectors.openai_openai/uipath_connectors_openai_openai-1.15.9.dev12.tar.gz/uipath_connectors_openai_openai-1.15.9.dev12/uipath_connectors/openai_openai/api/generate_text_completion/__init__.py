from .generate_text_completion import sync as generate_text_completion
from .generate_text_completion import asyncio as generate_text_completion_async

__all__ = [
    "generate_text_completion",
    "generate_text_completion_async",
]
