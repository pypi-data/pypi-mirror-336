import math
import nltk
from abc import ABC, abstractmethod

class Metric(ABC):
    """
    Abstract base class for all text evaluation metrics.
    Subclasses must implement the __call__ method.
    """
    def __init__(self):
        pass

    @abstractmethod
    def __call__(self, output: str) -> float:
        pass

class Perplexity(Metric):
    """
    Computes a custom perplexity-like score for a given text output.
    This implementation is not traditional perplexity from language modeling,
    but a heuristic based on average word length and repetition.

    Formula:
        perplexity = exp(avg_word_len * repetition_factor)

    - avg_word_len: average number of characters per word
    - repetition_factor: total tokens divided by unique tokens (higher means more repetition)
    """
    def __init__(self):
        super().__init__()

    def __call__(self, output: str) -> float:
        tokens = nltk.word_tokenize(output)

        if not tokens:
            return 0.0

        avg_word_len = sum(len(word) for word in tokens) / len(tokens)
        repetition_factor = len(tokens) / len(set(tokens))

        perplexity = math.exp(avg_word_len * repetition_factor)
        return round(perplexity, 2)

class LexicalDiversity(Metric):
    """
    Computes the lexical diversity of the given text output.

    Lexical diversity is defined as:
        diversity = number of unique tokens / total number of tokens

    Returns a value between 0.0 (low diversity) and 1.0 (high diversity).
    """
    def __init__(self):
        super().__init__()

    def __call__(self, output: str) -> float:
        tokens = nltk.word_tokenize(output)

        if not tokens:
            return 0.0

        diversity = len(set(tokens)) / len(tokens)
        return round(diversity, 4)