import itertools
import typing

from .openai_client import OpenAIClient
from .gemini_client import GeminiClient
from .ollama_client import OllamaClient
from .groq_client import GroqClient
from .anthropi_client import AnthropicClient
from .base import LLMSchema

class ModelsList:
    """
    A class for storing a list of models.
    """
    def __init__(self, models: typing.List[LLMSchema]):
        self.models = models

    def __iter__(self):
        return iter(self.models)

    def __len__(self):
        return len(self.models)

    def __getitem__(self, item):
        return self.models[item]

    def group_by(self, key: str):
        """
        Group models by a key.
        :param key: The key to group by.
        :return: A dictionary with the key as the key and the list of models as the value.
        """
        for group_key, group_items in itertools.groupby(self.models, lambda m: getattr(m, key)):
            yield group_key, list(group_items)

    def filter_by(self, key: str, value: str):
        """
        Filter models by a key.
        :param key: The key to filter by.
        :param value: The value to filter by.
        :return: A list of models that match the filter.
        """
        return ModelsList([model for model in self.models if getattr(model, key) == value])

    def __repr__(self):
        return "\n".join([f"{model.client}: {model.name}" for model in self.models])

class LLM:
    """
    A factory class for creating model instances.
    """

    _clients = {"openai": OpenAIClient, "google": GeminiClient, "ollama": OllamaClient, "groq": GroqClient, "anthropic": AnthropicClient}

    @staticmethod
    def available_models() -> ModelsList:
        """
        Get a list of available models.
        :return:
        """
        models = []
        for client_name, client_class in LLM._clients.items():
            try:
                models.extend(client_class.list_models())
            except:
                pass
        return ModelsList(models)

    @staticmethod
    def create(model: str, **kwargs):
        """
        Create a model instance.

        :param model: The model name to create an instance of.
        :param kwargs: Additional keyword arguments to pass to the model's `get_model` method.
        :return: The created model instance.
        :raises ValueError: If the model is not found in any client.
        """

        # Find the correct client based on the model name
        for client_name, client_class in LLM._clients.items():
            try:
                return client_class.get_model(model, **kwargs)
            except:
                pass
        # If the model is not found in any of the clients, raise an error
        raise ValueError(f"Model '{model}' is not available in any registered client.")
