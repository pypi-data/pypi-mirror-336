"""Dictionary-based text classifier using word matching and probability transformations.

This module provides a simple dictionary-based classifier that can perform
multi-class or multi-label classification based on word matching and probability
transformations using softmax or sigmoid functions.
"""

import json
import math
from pathlib import Path
from typing import Dict, List, Optional, Union


class DictionaryClassifier:
    """A dictionary-based text classifier using word matching and probability transformations.

    This classifier performs text classification by matching words against predefined
    dictionaries for each class/label. It supports both multi-class and multi-label
    classification through different probability transformations.

    Args:
        model_path: Optional path to a saved model directory
        classifier_type: Type of classification ('multi_class' or 'multi_label')
        label_dictionary: Dictionary mapping labels to lists of words
    """

    VALID_CLASSIFIER_TYPES = {"multi_class", "multi_label"}

    def __init__(
        self,
        model_path: Optional[Union[str, Path]] = None,
        classifier_type: str = "multi_class",
        label_dictionary: Optional[Dict[str, List[str]]] = None,
    ) -> None:
        if classifier_type not in self.VALID_CLASSIFIER_TYPES:
            raise ValueError(f"Unsupported classifier type: {classifier_type}")

        self.model_path = Path(model_path) if model_path else None
        self.round_value = 4
        self.classifier_type = classifier_type
        self.label_dictionary = (
            {k: sorted(list(set(v))) for k, v in label_dictionary.items()}
            if label_dictionary
            else None
        )

    def _format_predict_dict(self, pred_dict: Dict[str, float]) -> Dict[str, float]:
        """Round float values in prediction dictionary to specified precision.

        Args:
            pred_dict: Dictionary of predictions with float values

        Returns:
            Dictionary with rounded float values
        """
        return {k: round(float(v), self.round_value) for k, v in pred_dict.items()}

    def _transform_predict_dict(self, pred_dict: Dict[str, float]) -> Dict[str, float]:
        """Transform raw word counts into probabilities using softmax or sigmoid.

        Args:
            pred_dict: Dictionary of raw word counts

        Returns:
            Dictionary of transformed probabilities
        """
        if all(x == 0 for x in pred_dict.values()):
            prob_dict = {k: 0.0 for k in pred_dict.keys()}
            prob_dict["no_label"] = 1.0
            return prob_dict

        elif self.classifier_type == "multi_class":
            return dict(
                zip(pred_dict.keys(), self._softmax_array(list(pred_dict.values())))
            )

        elif self.classifier_type == "multi_label":
            return dict(
                zip(pred_dict.keys(), self._sigmoid_array(list(pred_dict.values())))
            )
        else:
            raise ValueError(f"Unsupported classifier type: {self.classifier_type}")

    def _sigmoid_array(self, x: List[float]) -> List[float]:
        """Apply sigmoid transformation to array of values.

        Args:
            x: List of values to transform

        Returns:
            List of sigmoid-transformed values
        """
        return [1 / (1 + math.exp(-e)) for e in x]

    def _softmax_array(self, x: List[float]) -> List[float]:
        """Apply softmax transformation to array of values.

        Args:
            x: List of values to transform

        Returns:
            List of softmax-transformed values
        """
        # Subtract max for numerical stability
        max_x = max(x)
        exp_x = [math.exp(val - max_x) for val in x]
        sum_exp = sum(exp_x)
        return [val / sum_exp for val in exp_x]

    def _get_label_word_count(self, text: str) -> Dict[str, int]:
        """Count occurrences of dictionary words in text.

        Args:
            text: Input text to analyze

        Returns:
            Dictionary mapping labels to word counts
        """
        if not self.label_dictionary:
            raise ValueError("Label dictionary not initialized")

        tally = {}
        for k, v in self.label_dictionary.items():
            tally_temp = sum(e in text.lower() for e in v)
            tally[k] = tally_temp

        return tally

    def from_disk(self, model_path: Union[str, Path]) -> None:
        """Load model configuration and label dictionary from disk.

        Args:
            model_path: Path to model directory

        Raises:
            FileNotFoundError: If model files don't exist
            json.JSONDecodeError: If JSON files are invalid
        """
        model_path = Path(model_path)
        try:
            with open(model_path / "config.json") as f:
                self.classifier_type = json.load(f)["classifier_type"]
            with open(model_path / "label_dictionary.json") as f:
                self.label_dictionary = json.load(f)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Model files not found in {model_path}") from e
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                "Invalid JSON in model files", e.doc, e.pos
            ) from e

    def to_disk(self, model_path: Union[str, Path]) -> None:
        """Save model configuration and label dictionary to disk.

        Args:
            model_path: Path to save model directory

        Raises:
            OSError: If directory creation or file writing fails
        """
        model_path = Path(model_path)
        try:
            model_path.mkdir(parents=True, exist_ok=True)
            with open(model_path / "config.json", "w") as f:
                json.dump({"classifier_type": self.classifier_type}, f)
            with open(model_path / "label_dictionary.json", "w") as f:
                json.dump(self.label_dictionary, f)
        except OSError as e:
            raise OSError(f"Failed to save model to {model_path}") from e

    def predict_single(self, text: str, round_preds: bool = True) -> Dict[str, float]:
        """Predict probabilities for a single text input.

        Args:
            text: Input text to classify
            round_preds: Whether to round probability values

        Returns:
            Dictionary mapping labels to probabilities

        Raises:
            ValueError: If label dictionary not initialized
        """
        if not self.label_dictionary:
            raise ValueError("Label dictionary not initialized")

        pred_dict = self._get_label_word_count(text)
        pred_dict = self._transform_predict_dict(pred_dict)
        return self._format_predict_dict(pred_dict) if round_preds else pred_dict

    def predict_batch(
        self, texts: List[str], round_preds: bool = True
    ) -> List[Dict[str, float]]:
        """Predict probabilities for a batch of text inputs.

        Args:
            texts: List of input texts to classify
            round_preds: Whether to round probability values

        Returns:
            List of dictionaries mapping labels to probabilities
        """
        return [self.predict_single(e, round_preds=round_preds) for e in texts]
