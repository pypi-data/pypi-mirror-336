import itertools
import os
import typing

import openai
import tenacity
from PIL.Image import Image as PILImage

from modihub.llm.base import LLMClient, LLMSchema
from modihub.utils import ImageUtils


class OpenAIClient(LLMClient):
    """A class for the OpenAI client."""

    def __init__(self, model_name: str, *args, **kwargs):
        super().__init__(model_name)
        self.system_instruction = kwargs.pop("system_instruction", "")
        self.api_client = OpenAIClient.get_api_client(*args, **kwargs)


    @staticmethod
    def get_api_client(*args, **kwargs) -> openai.OpenAI:
        """Configure the API key for the OpenAI client."""
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key is None:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        return openai.OpenAI(api_key=api_key, *args, **kwargs)

    def _normalized_prompt(self, prompt: typing.Any) -> typing.List[dict]:
        """
        Normalize the prompt.
        :param prompt:
        :return:
        """
        if isinstance(prompt, str):
            return [{"type": "text", "text": prompt}]
        elif isinstance(prompt, PILImage):
            return [
                {
                    "type": "image_url",
                    "image_url": {"url": ImageUtils.image_to_base64_url(prompt)},
                }
            ]
        elif isinstance(prompt, list):
            return list(
                itertools.chain.from_iterable(
                    self._normalized_prompt(p) for p in prompt
                )
            )
        else:
            raise ValueError("Unsupported prompt type")

    @tenacity.retry(wait=tenacity.wait_fixed(2), stop=tenacity.stop_after_attempt(3), reraise=True)
    def generate(self, prompt: typing.Any, *args, **kwargs) -> str:
        messages_queue = (
            [{"role": "system", "content": self.system_instruction}]
            if self.system_instruction
            else []
        )
        normalized_prompt = self._normalized_prompt(prompt)
        messages_queue.append({"role": "user", "content": normalized_prompt})
        completion = self.api_client.chat.completions.create(
            model=self.model_name, messages=messages_queue, **kwargs
        )
        return completion.choices[0].message.content

    @classmethod
    def list_models(cls, *args, **kwargs) -> typing.List[LLMSchema]:
        api_client = OpenAIClient.get_api_client(*args, **kwargs)
        available_models = api_client.models.list()
        return [
            LLMSchema(name=model_info.id, display_name=model_info.id, client="openai")
            for model_info in available_models
        ]


if __name__ == '__main__':
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())

    for m in OpenAIClient.list_models():
        print(m.name)
    response = OpenAIClient.get_model("gpt-4o-mini", system_instruction="generate the output in markdown format")
    print(response("who are you?"))