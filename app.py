"""
Flask Image Recognition Application
Handles image uploads, preprocessing, and prediction.
"""

from flask import Flask, render_template, request
from model import preprocess_img, predict_result

# Instantiate Flask app
app = Flask(__name__)


@app.route("/")
def main():
    """Render the home page."""
    return render_template("index.html")


@app.route("/prediction", methods=["POST"])
def predict_image_file():
    """Handle image upload and return prediction results."""
    try:
        if request.method == "POST":
            img = preprocess_img(request.files["file"].stream)
            pred = predict_result(img)
            return render_template("result.html", predictions=str(pred))
    except Exception:  # pylint: disable=broad-except
        error = "File cannot be processed."
        return render_template("result.html", err=error)


if __name__ == "__main__":
    # Run the app in debug mode on port 9000
    app.run(port=9000, debug=True)
