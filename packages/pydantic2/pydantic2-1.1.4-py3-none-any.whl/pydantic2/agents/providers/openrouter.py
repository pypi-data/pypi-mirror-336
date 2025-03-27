from typing import Dict, Any, Optional, List
from openai import AsyncOpenAI
from .base import ProviderBase

class OpenRouterProvider(ProviderBase):
    """OpenRouter provider implementation."""

    def __init__(
        self,
        api_key: str,
        model_name: str = "openai/gpt-4o-mini",
        base_url: str = "https://openrouter.ai/api/v1",
        headers: Optional[Dict[str, str]] = None
    ):
        """
        Initialize OpenRouter provider.

        Args:
            api_key: OpenRouter API key
            model_name: Model to use
            base_url: OpenRouter base URL
            headers: Additional headers
        """
        self.model_name = model_name

        # Build default headers
        default_headers = {
            "HTTP-Referer": "https://aiforma.app"  # For attribution
        }

        if headers:
            default_headers.update(headers)

        # Initialize client with proper headers
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url=base_url,
            default_headers=default_headers
        )

    async def invoke(
        self,
        system: str,
        user: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        response_format: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Invoke the model with system and user messages.

        Args:
            system: System message
            user: User message
            temperature: Temperature for sampling
            max_tokens: Maximum tokens to generate
            response_format: Response format specification

        Returns:
            OpenAI API response
        """
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ]

        # Create call without headers parameter
        response = await self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format=response_format
        )

        return response
