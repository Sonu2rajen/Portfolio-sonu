from flask import Flask, render_template, request
import os

import tensorflow as tf
from tensorflow.keras.models import load_model  # type: ignore
from tensorflow.keras.preprocessing import image  # type: ignore
from tensorflow.keras.metrics import AUC  # type: ignore
import numpy as np


app = Flask(__name__)


# ---------------------------------------------------------
# PROJECT PATHS
# ---------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "model", "skin.h5")
TESTS_DIR = os.path.join(BASE_DIR, "static", "tests")

# Make sure the tests folder exists
os.makedirs(TESTS_DIR, exist_ok=True)


# ---------------------------------------------------------
# MODEL / DEPENDENCIES
# ---------------------------------------------------------

dependencies = {
    "auc_roc": AUC
}


verbose_name = {
    0: "Actinic keratoses and intraepithelial carcinomae",
    1: "Basal cell carcinoma",
    2: "Benign keratosis-like lesions",
    3: "Dermatofibroma",
    4: "Melanocytic nevi",
    5: "Pyogenic granulomas and hemorrhage",
    6: "Melanoma",
}


# ---------------------------------------------------------
# LOAD MODEL
# ---------------------------------------------------------

model = load_model(MODEL_PATH)


# ---------------------------------------------------------
# PREDICTION FUNCTION
# ---------------------------------------------------------

def predict_label(img_path):
    test_image = image.load_img(
        img_path,
        target_size=(28, 28)
    )

    test_image = image.img_to_array(test_image) / 255.0

    test_image = test_image.reshape(
        1,
        28,
        28,
        3
    )

    predict_x = model.predict(test_image)

    classes_x = np.argmax(
        predict_x,
        axis=1
    )

    return verbose_name[classes_x[0]]


# ---------------------------------------------------------
# HOME
# ---------------------------------------------------------

@app.route("/")
@app.route("/first")
def first():
    return render_template("first.html")


# ---------------------------------------------------------
# LOGIN
# ---------------------------------------------------------

@app.route("/login")
def login():
    return render_template("login.html")


# ---------------------------------------------------------
# INDEX / UPLOAD PAGE
# ---------------------------------------------------------

@app.route("/index", methods=["GET", "POST"])
def index():
    return render_template("index.html")


# ---------------------------------------------------------
# IMAGE SUBMISSION / PREDICTION
# ---------------------------------------------------------

@app.route("/submit", methods=["GET", "POST"])
def get_output():

    if request.method == "POST":

        # Check whether a file was uploaded
        if "my_image" not in request.files:
            return "No image file was uploaded.", 400

        img = request.files["my_image"]

        # Check whether a filename exists
        if img.filename == "":
            return "No image was selected.", 400

        # Create a safe file path
        img_path = os.path.join(
            TESTS_DIR,
            img.filename
        )

        # Save uploaded image
        img.save(img_path)

        # Predict
        predict_result = predict_label(img_path)

        # Convert filesystem path to a URL path for the browser
        relative_img_path = os.path.relpath(
            img_path,
            BASE_DIR
        ).replace(os.sep, "/")

        relative_img_path = "/" + relative_img_path

        return render_template(
            "prediction.html",
            prediction=predict_result,
            img_path=relative_img_path
        )

    return render_template("index.html")


# ---------------------------------------------------------
# RUN APPLICATION
# ---------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)