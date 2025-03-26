# Clear BOW 📚

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Lightweight dictionary-based classifier that converts word frequencies into label probabilities using softmax/sigmoid functions. Perfect for bootstrapping classifications with terminology lists.

## Features
- 🔍 Dictionary-based classification
- 📊 Multi-class (softmax) support
- 🏷️ Multi-label (sigmoid) support
- 📝 Simple terminology lists
- 🔢 Probability outputs
- 💾 Model save/load functionality
- 🎯 93% test coverage

## Installation
```bash
# Via pip
pip install clear-bow

# Or from source
git clone https://github.com/samhardyhey/clear-bow
cd clear-bow
pip install -e .
```

## Usage
```python
from clear_bow.classifier import DictionaryClassifier

# Define your dictionary
super_dict = {
    "regulation": ["asic", "government", "federal", "tax"],
    "contribution": ["contribution", "concession", "personal", "after tax"],
    "fund": ["unisuper", "aus super", "sun super", "qsuper"],
}

# Create classifier (multi-class by default)
dc = DictionaryClassifier(label_dictionary=super_dict)

# Or for multi-label classification
dc = DictionaryClassifier(
    label_dictionary=super_dict,
    classifier_type="multi_label"
)

# Make predictions
result = dc.predict_single("A 10% contribution to your super fund")
# Returns probability distribution across labels

# Batch predictions
results = dc.predict_batch([
    "A 10% contribution to your super fund",
    "Government regulation of super funds"
])

# Save model to disk
dc.to_disk("path/to/model")

# Load model from disk
dc = DictionaryClassifier()
dc.from_disk("path/to/model")
```

## Development
```bash
# Setup development environment
make setup-local-dev
source venv/bin/activate

# Run tests
make test-local

# Run tests with coverage
make test-coverage

# Multi-environment testing
make test-tox

# Build distribution
make dist-bundle-build

# Clean build artifacts
make clean

# Upload to PyPI
make publish
```

## Project Structure
```
clear-bow/
├── src/
│   └── clear_bow/
│       ├── __init__.py
│       └── classifier.py
├── tests/
│   ├── conftest.py
│   └── test_classifier.py
├── pyproject.toml    # Project configuration
├── tox.ini          # Multi-environment testing
└── makefile         # Development commands
```

## Features in Detail

### Multi-class Classification
- Uses softmax transformation
- Outputs sum to 1.0
- Best for mutually exclusive categories

### Multi-label Classification
- Uses sigmoid transformation
- Each label gets independent probability
- Best for non-exclusive categories

### Error Handling
- Validates classifier types
- Handles missing/invalid files
- Provides informative error messages

### File Operations
- Save model configuration
- Save label dictionaries
- Load models from disk

*Note: See tests for additional usage examples and edge cases.*

## License
MIT License - See LICENSE file for details.