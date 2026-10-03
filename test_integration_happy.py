"""Test a successful upload using a supplied image."""

from pathlib import Path
import re


def test_successful_prediction(client):
    """A valid image should produce a numeric prediction without an error."""
    image_path = (
        Path(__file__).parent
        / "test_images"
        / "2"
        / "Sign 2 (97).jpeg"
    )

    with image_path.open("rb") as image_file:
        response = client.post(
            "/prediction",
            data={"file": (image_file, image_path.name)},
            content_type="multipart/form-data",
        )

    assert response.status_code == 200
    assert b"File cannot be processed." not in response.data

    html = response.get_data(as_text=True)
    assert re.search(r"<h2\b[^>]*>\s*\d+\s*</h2>", html)
