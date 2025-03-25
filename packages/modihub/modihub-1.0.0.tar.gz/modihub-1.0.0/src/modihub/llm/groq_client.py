import os
import typing
import logging
from functools import lru_cache

import groq
import tenacity
from groq import Groq

from modihub.llm.base import LLMClient, LLMSchema

logging.basicConfig(level=logging.INFO)

def api_exception_handler(func):
    """Decorator to handle exceptions from the API client."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except groq.APIConnectionError as e:
            logging.error(f"The server could not be reached: {e.__cause__}")
            raise RuntimeError(f"The server could not be reached: {e.__cause__}")
        except groq.RateLimitError as e:
            logging.error(f"The rate limit has been exceeded: {e.__cause__}")
            raise RuntimeError(f"The rate limit has been exceeded: {e.__cause__}")
        except groq.APIStatusError as e:
            logging.error(f"The server returned an error: {e.status_code}@{e.response}")
            raise RuntimeError(f"The server returned an error: {e.status_code}@{e.response}")
    return wrapper

class GroqClient(LLMClient):
    """Client for interacting with Groq models."""

    def __init__(self, model_name: str, *args, **kwargs) -> None:
        super().__init__(model_name)
        self.system_instruction = kwargs.pop("system_instruction", "")
        self.api_client = self._get_api_client( *args, **kwargs)


    @staticmethod
    def _get_api_client(*args, **kwargs) -> Groq:
        """Configure and return the Groq API client."""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")
        return Groq(api_key=api_key,*args, **kwargs)

    @tenacity.retry(wait=tenacity.wait_fixed(2), stop=tenacity.stop_after_attempt(3), reraise=True)
    @api_exception_handler
    def generate(self, prompt: str, *args, **kwargs) -> str:
        """Generate text from the model with retry logic."""
        messages_queue = (
            [{"role": "system", "content": self.system_instruction}]
            if self.system_instruction
            else []
        )
        messages_queue.append({"role": "user", "content": prompt})
        try:
            completion = self.api_client.chat.completions.create(
                model=self.model_name, messages=messages_queue, **kwargs
            )
            return completion.choices[0].message.content
        except Exception as e:
            logging.error(f"Error generating content: {e}")
            raise

    @classmethod
    @lru_cache(maxsize=1)
    def list_models(cls) -> typing.List[LLMSchema]:
        """Retrieve and cache available models from Groq."""
        api_client = cls._get_api_client()
        try:
            available_models = api_client.models.list().data
            return [
                LLMSchema(
                    client="groq",
                    name=model.id,
                    display_name=model.id
                )
                for model in available_models
            ]
        except Exception as e:
            logging.error(f"Failed to list models: {e}")
            return []

if __name__ == "__main__":
    from dotenv import load_dotenv, find_dotenv

    load_dotenv(find_dotenv())

    models = GroqClient.list_models()
    for model in models:
        print(model.name)

    try:
        client = GroqClient("llama3-8b-8192", system_instruction="Generate the output in markdown format")
        response = client.generate("Who are you?")
        print(response)
    except Exception as e:
        logging.error(f"Error during execution: {e}")
