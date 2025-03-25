import typing
from concurrent.futures import ThreadPoolExecutor, as_completed

# Assuming Metric and LLMClient classes are defined elsewhere
from modihub.metrics import Metric  # Update 'your_module' to the correct module name
from modihub.llm import LLM, LLMClient
class Evaluator:
    """
    Evaluator class for benchmarking multiple models on a given prompt using a list of metrics.
    """
    def __init__(self, models: typing.List[str], metrics: typing.List[Metric]):
        """
        Initializes the Evaluator with a list of model names and evaluation metrics.

        :param models: List of model identifiers (e.g., names or keys)
        :param metrics: List of Metric instances used to evaluate model output
        """
        self.models = models
        self.metrics = metrics

    def evaluate(self, prompt: str) -> typing.List[typing.Dict[str, float]]:
        """
        Evaluate all models on the given prompt.

        :param prompt: Text prompt to evaluate
        :return: List of dictionaries, each containing metric scores for a model
        """
        def evaluate_model(model: LLMClient, prompt: str) -> typing.Dict[str, float]:
            """
            Evaluate a single model's output using all metrics.

            :param model: An instance of LLMClient
            :param prompt: Text prompt for the model to respond to
            :return: Dictionary of metric name to score
            """
            output = model(prompt)
            return {
                metric.__class__.__name__: metric(output)
                for metric in self.metrics
            }

        results = []
        with ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(evaluate_model, LLM.create(model), prompt): model
                for model in self.models
            }
            for future in as_completed(futures):
                results.append(future.result())

        return results