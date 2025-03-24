import os
import tensorflow as tf
from .model import galaxy_morph, preprocess_image
from . import bpt  # Import the BPT module

# Get the absolute model path inside the package
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.keras")

# Load the model globally
if os.path.exists(MODEL_PATH):
    model = tf.keras.models.load_model(MODEL_PATH)
else:
    raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")

# Expose key functions and modules
__all__ = ["galaxy_morph", "preprocess_image", "model", "bpt"]
