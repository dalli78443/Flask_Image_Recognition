# test_acceptance_happy.py
"""Acceptance tests for happy path scenarios in image uploads."""

from io import BytesIO
import pytest
from app import app

@pytest.fixture
def client():
    """Flask test client fixture for happy path tests."""
    with app.test_client() as client:
        yield client

def simulate_image_upload(client, image_bytes, filename="test_image.jpg"):
    """Helper to simulate an image upload to the prediction endpoint."""
    img_data = BytesIO(image_bytes)
    img_data.name = filename

    response = client.post(
        "/prediction",
        data={"file": (img_data, img_data.name)},
        content_type="multipart/form-data"
    )
    return response

def test_successful_upload(client):
    """Check that a valid image upload returns a prediction."""
    response = simulate_image_upload(client, b"fake_image_data", "test_image.jpg")
    assert response.status_code == 200
    assert b"Prediction" in response.data

def test_valid_large_image(client):
    """Check that a large valid image file is processed correctly."""
    response = simulate_image_upload(
        client,
        b"fake_large_image_data" * 1000,
        "large_image.jpg"
    )
    assert response.status_code == 200
    assert b"Prediction" in response.data

def test_valid_image_size_upload(client):
    """Check that a specific large-size image file is processed correctly."""
    response = simulate_image_upload(
        client,
        b"valid_image_data_of_large_size" * 1000,
        "large_image.jpg"
    )
    assert response.status_code == 200
    assert b"Prediction" in response.data
#additional
def test_multiple_sequential_uploads(client):
    """Ensure multiple valid image uploads in sequence succeed."""
    filenames = ["image1.jpg", "image2.jpg", "image3.jpg"]
    for name in filenames:
        response = simulate_image_upload(client, b"valid_image_data", name)
        assert response.status_code == 200
        assert b"Prediction" in response.data
