# test_integration_sad.py

import pytest
from app import app
from io import BytesIO

@pytest.fixture
def client():
    """Fixture for the Flask test client."""
    with app.test_client() as client:
        yield client

def test_missing_file(client):
    """Test the prediction route with a missing file."""
    response = client.post("/prediction", data={}, content_type="multipart/form-data")
    assert response.status_code == 200
    assert b"File cannot be processed." in response.data  # Check if the error message is displayed


#additional test
def test_invalid_file_upload(client):
    """
    Test the prediction route with an invalid/corrupted file.
    - Purpose: Ensure the application handles non-image uploads correctly.
    """
    invalid_file = BytesIO(b"this_is_not_an_image")
    invalid_file.name = "not_an_image.txt"

    response = client.post(
        "/prediction",
        data={"file": (invalid_file, invalid_file.name)},
        content_type="multipart/form-data"
    )

    assert response.status_code == 200
    assert b"File cannot be processed." in response.data  # Expected error message
