"""Tests for the DictionaryClassifier class."""

import json

import pytest

from clear_bow.classifier import DictionaryClassifier


class TestDictionaryClassifierInitialization:
    """Test cases for DictionaryClassifier initialization."""

    def test_init_with_defaults(self):
        """Test initialization with default values."""
        dc = DictionaryClassifier()
        assert dc.classifier_type == "multi_class"
        assert dc.label_dictionary is None
        assert dc.round_value == 4

    def test_init_with_custom_values(self, super_dictionary):
        """Test initialization with custom values."""
        dc = DictionaryClassifier(
            classifier_type="multi_label", label_dictionary=super_dictionary
        )
        assert dc.classifier_type == "multi_label"
        assert dc.label_dictionary == super_dictionary
        assert dc.round_value == 4

    def test_init_with_invalid_classifier_type(self):
        """Test initialization with invalid classifier type."""
        with pytest.raises(ValueError, match="Unsupported classifier type"):
            DictionaryClassifier(classifier_type="invalid_type")


class TestDictionaryClassifierPredictions:
    """Test cases for DictionaryClassifier prediction methods."""

    def test_multi_class_single_simple(self, super_dictionary, example_doc):
        """Test single prediction with multi-class classifier."""
        dc = DictionaryClassifier(label_dictionary=super_dictionary)
        pred = dc.predict_single(example_doc)

        # Check keys
        key_set = set(super_dictionary.keys())
        key_set.add("no_label")
        assert set(pred.keys()).issubset(key_set)

        # Check probabilities
        assert sum(pred.values()) <= 1.0  # softmax sum <= 1
        assert all(0 <= v <= 1 for v in pred.values())
        assert all(isinstance(v, float) for v in pred.values())

    def test_multi_class_batch_simple(self, super_dictionary, example_docs):
        """Test batch prediction with multi-class classifier."""
        dc = DictionaryClassifier(label_dictionary=super_dictionary)
        preds = dc.predict_batch(example_docs)

        for pred in preds:
            key_set = set(super_dictionary.keys())
            key_set.add("no_label")
            assert set(pred.keys()).issubset(key_set)
            assert sum(pred.values()) <= 1.0
            assert all(0 <= v <= 1 for v in pred.values())

    def test_multi_label_single_simple(self, super_dictionary, example_doc):
        """Test single prediction with multi-label classifier."""
        dc = DictionaryClassifier(
            classifier_type="multi_label", label_dictionary=super_dictionary
        )
        pred = dc.predict_single(example_doc)

        assert set(pred.keys()) == set(super_dictionary.keys())
        assert all(0.5 <= v <= 1.0 for v in pred.values())
        assert all(isinstance(v, float) for v in pred.values())

    def test_multi_label_batch_simple(self, super_dictionary, example_docs):
        """Test batch prediction with multi-label classifier."""
        dc = DictionaryClassifier(
            classifier_type="multi_label", label_dictionary=super_dictionary
        )
        preds = dc.predict_batch(example_docs)

        for pred in preds:
            assert set(pred.keys()) == set(super_dictionary.keys())
            assert all(0.5 <= v <= 1.0 for v in pred.values())

    def test_empty_text(self, super_dictionary):
        """Test prediction with empty text."""
        dc = DictionaryClassifier(label_dictionary=super_dictionary)
        pred = dc.predict_single("")

        assert all(v == 0.0 for k, v in pred.items() if k != "no_label")
        assert pred["no_label"] == 1.0

    def test_no_matches(self, super_dictionary):
        """Test prediction with text containing no dictionary words."""
        dc = DictionaryClassifier(label_dictionary=super_dictionary)
        pred = dc.predict_single("This text contains no matching words")

        assert all(v == 0.0 for k, v in pred.items() if k != "no_label")
        assert pred["no_label"] == 1.0


class TestDictionaryClassifierFileOperations:
    """Test cases for DictionaryClassifier file operations."""

    @pytest.fixture
    def temp_model_dir(self, tmp_path):
        """Create a temporary directory for model files."""
        return tmp_path / "model"

    def test_save_and_load(self, super_dictionary, temp_model_dir):
        """Test saving and loading model files."""
        # Create and save model
        dc = DictionaryClassifier(label_dictionary=super_dictionary)
        dc.to_disk(temp_model_dir)

        # Verify files exist
        assert (temp_model_dir / "config.json").exists()
        assert (temp_model_dir / "label_dictionary.json").exists()

        # Load model
        new_dc = DictionaryClassifier()
        new_dc.from_disk(temp_model_dir)

        # Verify loaded model matches original
        assert new_dc.classifier_type == dc.classifier_type
        assert new_dc.label_dictionary == dc.label_dictionary

    def test_load_nonexistent_file(self, tmp_path):
        """Test loading from nonexistent directory."""
        dc = DictionaryClassifier()
        with pytest.raises(FileNotFoundError):
            dc.from_disk(tmp_path / "nonexistent")

    def test_load_invalid_json(self, temp_model_dir):
        """Test loading invalid JSON files."""
        # Create directory and invalid JSON file
        temp_model_dir.mkdir(parents=True, exist_ok=True)
        with open(temp_model_dir / "config.json", "w") as f:
            f.write("invalid json")

        dc = DictionaryClassifier()
        with pytest.raises(json.JSONDecodeError):
            dc.from_disk(temp_model_dir)


class TestDictionaryClassifierMath:
    """Test cases for DictionaryClassifier mathematical operations."""

    def test_softmax_array(self):
        """Test softmax transformation."""
        dc = DictionaryClassifier()
        x = [1.0, 2.0, 3.0]
        result = dc._softmax_array(x)

        # Check properties of softmax
        assert len(result) == len(x)
        assert all(0 <= v <= 1 for v in result)
        assert abs(sum(result) - 1.0) < 1e-10
        assert result[2] > result[1] > result[0]  # preserves order

    def test_sigmoid_array(self):
        """Test sigmoid transformation."""
        dc = DictionaryClassifier()
        x = [-1.0, 0.0, 1.0]
        result = dc._sigmoid_array(x)

        # Check properties of sigmoid
        assert len(result) == len(x)
        assert all(0 <= v <= 1 for v in result)
        assert result[1] == 0.5  # sigmoid(0) = 0.5
        assert result[2] > 0.5  # sigmoid(1) > 0.5
        assert result[0] < 0.5  # sigmoid(-1) < 0.5

    def test_format_predict_dict(self):
        """Test prediction dictionary formatting."""
        dc = DictionaryClassifier()
        pred_dict = {"a": 1.2345678, "b": 2.3456789}
        result = dc._format_predict_dict(pred_dict)

        assert all(isinstance(v, float) for v in result.values())
        assert all(len(str(v).split(".")[1]) <= 4 for v in result.values())
        assert result["a"] == 1.2346
        assert result["b"] == 2.3457
