import os
import typing

import anthropic
import tenacity
from anthropic import Anthropic
from modihub.llm.base import LLMClient, LLMSchema


def api_exception_handler(func):
    """
    Decorator to handle and translate Anthropic API errors into user-friendly runtime exceptions.
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except anthropic.AnthropicError as e:
            raise RuntimeError(f"Anthropic API error: {e}") from e
        except anthropic.RateLimitError as e:
            raise RuntimeError(f"Rate limit exceeded: {e.__cause__}") from e

    return wrapper


class AnthropicClient(LLMClient):
    """
    A client wrapper for interacting with Anthropic's Claude models.

    Supports system instructions, retries on failure, and model listing.
    """

    def __init__(self, model_name: str, *args, **kwargs) -> None:
        """
        Initialize the Anthropic client.

        Args:
            model_name (str): The Claude model to use (e.g., "claude-3-sonnet").
            system_instruction (str, optional): Context for Claude's behavior.
        """
        super().__init__(model_name)
        self.system_instruction = kwargs.pop("system_instruction", "")
        self.api_client = self.get_api_client(*args, **kwargs)

    @staticmethod
    def get_api_client(*args, **kwargs) -> Anthropic:
        """
        Creates and returns an authenticated Anthropic API client.

        Returns:
            Anthropic: An instance of the Anthropic client.

        Raises:
            ValueError: If ANTHROPIC_API_KEY is not set in the environment.
        """
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is not set")
        return Anthropic(api_key=api_key, *args, **kwargs)

    @tenacity.retry(wait=tenacity.wait_fixed(2), stop=tenacity.stop_after_attempt(3), reraise=True)
    @api_exception_handler
    def generate(self, prompt: str, *args, **kwargs) -> str:
        """
        Generates a response from Claude based on a user prompt.

        Args:
            prompt (str): The user's input prompt.
            max_tokens (int): Maximum tokens to generate (default: 1024).
            **kwargs: Additional generation parameters (e.g., temperature).

        Returns:
            str: Generated response content from Claude.
        """
        messages = [{"role": "system", "content": self.system_instruction}] if self.system_instruction else []
        messages.append({"role": "user", "content": prompt})

        response = self.api_client.messages.create(
            model=self.model_name,
            messages=messages,
            max_tokens=kwargs.pop("max_tokens", 1024),
            **kwargs
        )

        return response.content[0] if response.content else ""

    @classmethod
    def list_models(cls, *args, **kwargs) -> typing.List[LLMSchema]:
        """
        Lists available Claude models.

        Returns:
            List[LLMSchema]: List of Claude models with metadata.
        """
        api_client = cls.get_api_client(*args, **kwargs)
        models = api_client.models.list()
        return [
            LLMSchema(
                name=model.id,
                display_name=model.display_name,
                client="anthropic"
            )
            for model in models
        ]


# === Example usage ===
if __name__ == "__main__":
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())

    print("📦 Available Claude Models:")
    for model in AnthropicClient.list_models():
        print(f"- {model.name}")

    # Create client instance with system instruction
    model_instance = AnthropicClient.get_model(
        "claude-3-7-sonnet-20250219",
        system_instruction="Generate the output in markdown format."
    )

    # Run generation
    try:
        print("\n🤖 Claude's Response:\n")
        print(model_instance("Who are you?"))
    except Exception as e:
        print(f"❌ Error: {e}")
