import typing

import ollama
import tenacity
from PIL.Image import Image as PILImage

from modihub.llm.base import LLMClient, LLMSchema
from modihub.utils import ImageUtils


class OllamaClient(LLMClient):
    """
    A client class for interacting with locally hosted Ollama LLMs.

    Supports multimodal inputs (text and images) and provides retry logic for robustness.
    """

    def __init__(self, model_name: str, *args, **kwargs) -> None:
        """
        Initialize the OllamaClient.

        Args:
            model_name (str): The name of the model to interact with.
            system_instruction (str, optional): An optional system prompt for context.
        """
        super().__init__(model_name)
        self.system_instruction = kwargs.pop("system_instruction", "")
        self.api_client = OllamaClient.get_api_client(*args, **kwargs)

    @staticmethod
    def get_api_client(*args, **kwargs) -> ollama.Client:
        """
        Initializes and returns the Ollama API client.

        Returns:
            ollama.Client: The Ollama API client instance.
        """
        return ollama.Client(*args, **kwargs)

    @staticmethod
    def _normalized_prompt_content(prompt: typing.Any) -> dict:
        """
        Normalizes the prompt to a message dictionary expected by Ollama.

        Supports:
            - Single string prompt
            - Single PIL Image
            - List of mixed strings and PIL Images

        Args:
            prompt (Any): The prompt input to normalize.

        Returns:
            dict: A message dict with role, content, and optionally images.

        Raises:
            ValueError: If the input type is not supported.
        """
        if isinstance(prompt, str):
            return {"role": "user", "content": prompt}

        elif isinstance(prompt, PILImage):
            return {
                "role": "user",
                "content": "",
                "images": [ImageUtils.image_to_base64_url(prompt)],
            }

        elif isinstance(prompt, list):
            images = [img for img in prompt if isinstance(img, PILImage)]
            texts = [txt for txt in prompt if isinstance(txt, str)]
            return {
                "role": "user",
                "content": "".join(texts),
                "images": [ImageUtils.image_to_base64(img) for img in images],
            }

        raise ValueError("Unsupported prompt type")

    @tenacity.retry(wait=tenacity.wait_fixed(2), stop=tenacity.stop_after_attempt(3), reraise=True)
    def generate(self, prompt: typing.Any, *args, **kwargs) -> str:
        """
        Generates a response from the Ollama model.

        Args:
            prompt (Any): Prompt content; can be string, PIL image, or a list of both.

        Returns:
            str: The response content from the model.
        """
        # Prepare the message queue with optional system instruction
        messages_queue = (
            [{"role": "system", "content": self.system_instruction}]
            if self.system_instruction
            else []
        )
        # Append normalized user message
        normalized_prompt = self._normalized_prompt_content(prompt)
        messages_queue.append(normalized_prompt)

        # Call the model
        response = self.api_client.chat(
            model=self.model_name,
            messages=messages_queue,
            **kwargs
        )

        ai_message = response.get("message", {})
        return ai_message.get("content", "")

    @staticmethod
    def list_models(*args, **kwargs) -> typing.List[LLMSchema]:
        """
        Lists all available models from the local Ollama server.

        Returns:
            List[LLMSchema]: List of models wrapped in LLMSchema format.
        """
        api_client = OllamaClient.get_api_client(*args, **kwargs)
        ollama_models = api_client.list()
        return [
            LLMSchema(
                name=model_info["model"],
                display_name=model_info["model"],
                client="ollama"
            )
            for model_info in ollama_models["models"]
        ]


# Example usage
if __name__ == '__main__':
    # List all available models
    print("Available Ollama Models:")
    for model in OllamaClient.list_models():
        print(f"- {model.name}")

    # Create an instance of the OllamaClient
    client = OllamaClient.get_model("llama3.1:latest", system_instruction="Generate the output in markdown format")

    # Generate a response from the model
    response = client.generate("Who are you?")
    print("\nModel Response:\n")
    print(response)
