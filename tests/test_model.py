"""
Unit tests for the image recognition model.
Covers preprocessing, prediction, and consistency checks.
"""

import pytest
import numpy as np
from keras.models import load_model
from model import preprocess_img, predict_result


@pytest.fixture(scope="module")
def model():
    """Load the trained model once for all tests."""
    return load_model("digit_model.h5")  # Adjust path if necessary


# ====================
# Basic Function Tests
# ====================

def test_preprocess_img():
    """Ensure the preprocess_img function processes correctly."""
    img_path = "test_images/2/Sign 2 (97).jpeg"
    processed_img = preprocess_img(img_path)

    # Output shape should match expected dimensions
    assert processed_img.shape == (1, 224, 224, 3), \
        "Processed image shape should be (1, 224, 224, 3)"

    # Values must be normalized between 0 and 1
    assert np.min(processed_img) >= 0 and np.max(processed_img) <= 1, \
        "Image pixel values should be normalized between 0 and 1"


def test_predict_result(model):
    """Verify predict_result returns an integer prediction."""
    img_path = "test_images/4/Sign 4 (92).jpeg"
    processed_img = preprocess_img(img_path)

    prediction = predict_result(processed_img)
    print(f"Prediction output: {prediction} (Type: {type(prediction)})")

    assert isinstance(prediction, (int, np.integer)), \
        "Prediction should be an integer class index"


# ======================
# Advanced Edge Case Tests
# ======================

def test_invalid_image_path():
    """Ensure preprocess_img raises FileNotFoundError for bad paths."""
    with pytest.raises(FileNotFoundError):
        preprocess_img("invalid/path/to/image.jpeg")


def test_image_shape_on_prediction(model):
    """Confirm predictions work for valid images."""
    img_path = "test_images/5/Sign 5 (86).jpeg"
    processed_img = preprocess_img(img_path)

    prediction = predict_result(processed_img)
    assert isinstance(prediction, (int, np.integer)), \
        "The prediction should be an integer"


def test_model_predictions_consistency(model):
    """Check that predictions for the same image are consistent."""
    img_path = "test_images/7/Sign 7 (54).jpeg"
    processed_img = preprocess_img(img_path)

    predictions = [predict_result(processed_img) for _ in range(5)]

    assert all(p == predictions[0] for p in predictions), \
        "Predictions for the same input should be consistent"
