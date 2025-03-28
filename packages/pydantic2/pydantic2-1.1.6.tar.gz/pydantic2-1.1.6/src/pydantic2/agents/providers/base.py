from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod

class ProviderBase(ABC):
    """Base interface for LLM providers."""

    @abstractmethod
    async def invoke(
        self,
        system: str,
        user: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        response_format: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Invoke the LLM with a system and user message.

        Args:
            system: System message
            user: User message
            temperature: Temperature for sampling
            max_tokens: Maximum tokens to generate
            response_format: Response format specification

        Returns:
            LLM response
        """
        pass
