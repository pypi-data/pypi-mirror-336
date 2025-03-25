import os
import typing
import logging
from functools import lru_cache
from time import sleep

import tenacity
from google import genai
from modihub.llm.base import LLMClient, LLMSchema
from google.genai.types import (
    GenerateImagesResponse,
    GenerateContentResponse,
    GenerateVideosOperation,
    EmbedContentResponse,
    GenerateContentConfigOrDict,
    GenerateContentConfig,
)

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GeminiClient(LLMClient):
    """
    A client wrapper for Google Gemini APIs supporting text, image, video, and embedding generation.

    Inherits:
        LLMClient: Base abstraction for unified LLM interface.
    """

    def __init__(self, model_name: str, *args, **kwargs) -> None:
        """
        Initialize the Gemini client with model name and optional system instruction.

        Args:
            model_name (str): The name of the Gemini model (e.g., 'gemini-pro').
            system_instruction (str, optional): Instruction to guide generation behavior.
        """
        super().__init__(model_name)
        self.model_name = model_name
        self.system_instruction = kwargs.pop("system_instruction", None)
        self.api_client = GeminiClient.get_api_client(*args, **kwargs)

    @staticmethod
    def get_api_client(*args, **kwargs) -> genai.Client:
        """
        Initializes the Google GenAI client using the environment API key.

        Returns:
            genai.Client: Configured GenAI client.

        Raises:
            ValueError: If 'GEMINI_API_KEY' is not set in the environment.
        """
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set")
        return genai.Client(api_key=api_key, *args, **kwargs)

    @tenacity.retry(wait=tenacity.wait_fixed(2), stop=tenacity.stop_after_attempt(3), reraise=True)
    def generate(self, prompt: str, *args, **kwargs) -> typing.Any:
        """
        Generates content from the Gemini model based on the modality.

        Supported modalities:
            - TEXT (default)
            - IMAGE
            - VIDEO
            - EMBEDDINGS

        Args:
            prompt (str): Prompt input to the model.
            modality (str): The content type to generate (TEXT, IMAGE, VIDEO, EMBEDDINGS).

        Returns:
            Any: The generated content based on modality.

        Raises:
            RuntimeError: If video generation fails.
            AssertionError: If prompt format is incorrect for given modality.
        """
        try:
            modality = kwargs.get("modality", "TEXT").upper()

            if modality == "IMAGE":
                assert isinstance(prompt, str), "Prompt must be a string for image generation"
                response: GenerateImagesResponse = self.api_client.models.generate_images(
                    model=self.model_name,
                    prompt=prompt,
                    **kwargs
                )
                return response.generated_images

            elif modality == "VIDEO":
                assert isinstance(prompt, str), "Prompt must be a string for video generation"
                gen_video_op: GenerateVideosOperation = self.api_client.models.generate_videos(
                    model=self.model_name,
                    prompt=prompt,
                    **kwargs
                )
                # Polling until video generation completes
                while not gen_video_op.done:
                    sleep(5)
                    gen_video_op = self.api_client.operations.get(gen_video_op)
                    if gen_video_op.error:
                        raise RuntimeError(f"Video generation failed: {gen_video_op.error}")
                return gen_video_op.result.generated_videos

            elif modality == "EMBEDDINGS":
                response: EmbedContentResponse = self.api_client.models.embed_content(
                    model=self.model_name,
                    contents=prompt,
                    **kwargs
                )
                return response

            else:  # Default is TEXT
                config: GenerateContentConfigOrDict = kwargs.pop("config", {})
                if isinstance(config, GenerateContentConfig):
                    config = config.to_json_dict()

                # Merge system_instruction into config if not already set
                if self.system_instruction and "system_instruction" not in config:
                    config["system_instruction"] = self.system_instruction

                response: GenerateContentResponse = self.api_client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=config
                )
                return response.text if hasattr(response, "text") else response

        except Exception as e:
            logger.error(f"[GeminiClient] Error generating content: {e}")
            raise

    @classmethod
    @lru_cache(maxsize=1)
    def list_models(cls, *args, **kwargs) -> typing.List[LLMSchema]:
        """
        Lists available Gemini models and caches the result.

        Returns:
            List[LLMSchema]: Models wrapped in LLMSchema format.
        """
        try:
            api_client = cls.get_api_client()
            available_models = api_client.models.list(*args, **kwargs)

            return [
                LLMSchema(
                    name=model_info.name,
                    display_name=model_info.display_name,
                    description=model_info.description,
                    client="google",
                )
                for model_info in available_models
                if hasattr(model_info, "supported_actions") and (
                    "generateContent" in model_info.supported_actions or
                    "embedContent" in model_info.supported_actions
                )
            ]
        except Exception as e:
            logger.error(f"[GeminiClient] Failed to list models: {e}")
            return []


# === Example usage ===
if __name__ == "__main__":
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())

    # List models
    print("🔍 Available Gemini Models:")
    for model in GeminiClient.list_models():
        print(f"- {model.name}")

    # Example: Generate a Spanish response
    try:
        client = GeminiClient.get_model(
            "models/gemini-2.0-flash-exp",
            system_instruction="generate the output in Spanish"
        )
        response = client.generate("Tell me a joke about AI.")
        print("\n🤖 Gemini Response:\n")
        print(response)
    except Exception as e:
        logger.error(f"❌ Error during generation: {e}")
