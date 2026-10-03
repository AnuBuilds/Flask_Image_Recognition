"""Test the home page and an expected prediction response."""

from io import BytesIO
from unittest.mock import Mock

from PIL import Image
import app as app_module


def test_home_page(client):
    """The home page should load successfully."""
    response = client.get("/")

    assert response.status_code == 200
    assert b"Hand Sign Digit" in response.data


def test_valid_upload_expected_response(client, monkeypatch):
    """A valid image should display the result returned by prediction."""
    image_data = BytesIO()
    Image.new("RGB", (224, 224), color="white").save(
        image_data, format="PNG"
    )
    image_data.seek(0)

    prediction_mock = Mock(return_value=5)
    monkeypatch.setattr(app_module, "predict_result", prediction_mock)

    response = client.post(
        "/prediction",
        data={"file": (image_data, "test.png")},
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    assert b"File cannot be processed." not in response.data
    assert (
        b'<h2 class="display-4 text-dark font-weight-bold">5</h2>'
        in response.data
    )

    prediction_mock.assert_called_once()
    processed_image = prediction_mock.call_args.args[0]
    assert processed_image.shape == (1, 224, 224, 3)
