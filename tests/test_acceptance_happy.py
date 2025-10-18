
# test_acceptance_happy.py

"""Acceptance tests for happy path scenarios in image
upload and prediction."""
from io import BytesIO
import pytest
from app import app

@pytest.fixture
def client():
    """Flask test client fixture for happy path tests."""
    with app.test_client() as client:
        yield client

def simulate_image_upload(client, image_bytes, filename="test_image.jpg"):
    """Helper to simulate an image upload to the
    prediction endpoint."""
    img_data = BytesIO(image_bytes)
    img_data.name = filename

    response = client.post(
        "/prediction",
        data={"file": (img_data, img_data.name)},
        content_type="multipart/form-data"
    )
    return response


def test_acceptance_successful_upload(client):
    """
    Test Case: Successful Upload of a Valid Image File
    - Purpose: Ensure the application accepts a valid image
    file upload and provides a prediction.
    """
    response = simulate_image_upload(client, b"fake_image_data", "test_image.jpg")

    assert response.status_code == 200
    assert b"Prediction" in response.data


def test_acceptance_valid_large_image(client):
    """
    Test Case: Upload of a Valid Large Image File
    - Purpose: Check if the system accepts large but
          valid image files without errors and
          still provides predictions.
    """
    response = simulate_image_upload(
        client,
        b"fake_large_image_data" * 1000,
        "large_image.jpg"
    )

    assert response.status_code == 200
    assert b"Prediction" in response.data

def test_acceptance_valid_image_size_upload(client):
    """
    Test Case: Upload of an Image with a Specific Large Size
    - Purpose: Validate system behavior with valid image
    files of a specific size or resolution.
    """
    response = simulate_image_upload(
        client,
        b"valid_image_data_of_large_size" * 1000,
        "large_image.jpg"
    )

    assert response.status_code == 200
    assert b"Prediction" in response.data

def test_acceptance_multiple_sequential_uploads(client):
    """
    Test Case: Multiple Sequential Uploads of Valid Images
    - Purpose: Ensure the system can handle several valid
      image uploads one after another without errors.
    """
    filenames = ["image1.jpg", "image2.jpg", "image3.jpg"]
    for name in filenames:
        response = simulate_image_upload(client, b"valid_image_data", name)
        assert response.status_code == 200
        assert b"Prediction" in response.data
