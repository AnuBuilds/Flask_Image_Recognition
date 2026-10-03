"""Load the trained model and prepare images for digit prediction."""

from keras.models import load_model
from keras.utils import img_to_array
import numpy as np
from PIL import Image

model = load_model("digit_model.h5")


def preprocess_img(img_path):
    """Resize and normalize an RGB image into the model's input shape."""
    with Image.open(img_path) as image:
        resized_image = image.resize((224, 224))
        image_array = img_to_array(resized_image) / 255.0

    return image_array.reshape(1, 224, 224, 3)


def predict_result(image_batch):
    """Return the class index with the highest prediction score."""
    predictions = model.predict(image_batch)
    return np.argmax(predictions[0], axis=-1)
