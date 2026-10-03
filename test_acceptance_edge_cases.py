"""Test invalid and empty image uploads."""

from io import BytesIO
from unittest.mock import Mock

import pytest
import app as app_module


@pytest.mark.parametrize(
    "file_content, filename",
    [
        (b"this is not an image", "invalid.jpg"),
        (b"", "empty.png"),
    ],
)
def test_invalid_upload(client, monkeypatch, file_content, filename):
    """Invalid image data should show an error without calling prediction."""
    prediction_mock = Mock()
    monkeypatch.setattr(app_module, "predict_result", prediction_mock)

    response = client.post(
        "/prediction",
        data={"file": (BytesIO(file_content), filename)},
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    assert b"File cannot be processed." in response.data
    prediction_mock.assert_not_called()
