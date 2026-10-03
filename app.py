"""Serve the hand-sign image upload and prediction pages."""

from flask import Flask, render_template, request
from werkzeug.exceptions import BadRequestKeyError

from model import preprocess_img, predict_result

app = Flask(__name__)


@app.route("/")
def main():
    """Display the image upload page."""
    return render_template("index.html")


@app.route("/prediction", methods=["POST"])
def predict_image_file():
    """Process an uploaded image and display its prediction or an error."""
    try:
        uploaded_file = request.files["file"]
        image = preprocess_img(uploaded_file.stream)
        prediction = predict_result(image)
    except (BadRequestKeyError, OSError, ValueError):
        return render_template(
            "result.html",
            err="File cannot be processed.",
        )

    return render_template("result.html", predictions=str(prediction))


if __name__ == "__main__":
    app.run(port=9000, debug=True)
