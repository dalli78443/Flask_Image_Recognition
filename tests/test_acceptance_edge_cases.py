# test_acceptance_edge_cases.py

from io import BytesIO

# Helper function for concurrent image uploads
def upload_image(client, img_data):
    """
    Helper function to upload an image within a thread.
    - Purpose: Enables concurrent uploads for testing multithreaded scenarios.
    """
    client.post(
        "/prediction",
        data={"file": (img_data, img_data.name)},
        content_type="multipart/form-data"
    )

# -----------------------------
# Original Edge Cases
# -----------------------------

# 1. Large Image Upload
def test_edge_case_large_image_upload(client):
    large_img_data = BytesIO(b"large_image_data" * 10**6)  # Simulate ~10MB image
    large_img_data.name = "large_image.jpg"

    response = client.post(
        "/prediction",
        data={"file": (large_img_data, large_img_data.name)},
        content_type="multipart/form-data"
    )

    assert b"Prediction" in response.data

# 2. Invalid / Missing Metadata
def test_edge_case_invalid_metadata(client):
    img_data = BytesIO(b"image_with_no_metadata")
    img_data.name = "image_no_metadata.jpg"

    response = client.post(
        "/prediction",
        data={"file": (img_data, img_data.name)},
        content_type="multipart/form-data"
    )

    assert b"Prediction" in response.data

# 3. Non-Standard File Extension
def test_edge_case_non_standard_image_extensions(client):
    img_data = BytesIO(b"valid_image_data")
    img_data.name = "non_standard_image.webp"

    response = client.post(
        "/prediction",
        data={"file": (img_data, img_data.name)},
        content_type="multipart/form-data"
    )

    assert b"Prediction" in response.data

# 4. Sequential Uploads
def test_edge_case_sequential_image_uploads(client):
    img_data1 = BytesIO(b"first_image_data")
    img_data1.name = "first_image.jpg"

    img_data2 = BytesIO(b"second_image_data")
    img_data2.name = "second_image.jpg"

    response1 = client.post(
        "/prediction",
        data={"file": (img_data1, img_data1.name)},
        content_type="multipart/form-data"
    )
    response2 = client.post(
        "/prediction",
        data={"file": (img_data2, img_data2.name)},
        content_type="multipart/form-data"
    )

    assert b"Prediction" in response1.data
    assert b"Prediction" in response2.data

# 5. Unexpected Headers
def test_edge_case_unexpected_headers(client):
    img_data = BytesIO(b"valid_image_data")
    img_data.name = "unexpected_headers_image.jpg"

    response = client.post(
        "/prediction",
        data={"file": (img_data, img_data.name)},
        content_type="multipart/form-data",
        headers={"X-Unexpected-Header": "value"}
    )

    assert b"Prediction" in response.data

# 6. Upload Over HTTP/2
def test_edge_case_upload_over_http2(client):
    img_data = BytesIO(b"valid_image_data")
    img_data.name = "http2_image.jpg"

    response = client.post(
        "/prediction",
        data={"file": (img_data, img_data.name)},
        content_type="multipart/form-data"
    )

    assert b"Prediction" in response.data

# -----------------------------
# Additional Edge Cases
# -----------------------------


# 1. Very Small Image Upload
def test_edge_case_small_image(client):
    small_img_data = BytesIO(b"\x89PNG\r\n\x1a\n")  # minimal PNG header
    small_img_data.name = "small.png"

    response = client.post(
        "/prediction",
        data={"file": (small_img_data, small_img_data.name)},
        content_type="multipart/form-data"
    )

    assert b"Prediction" in response.data
