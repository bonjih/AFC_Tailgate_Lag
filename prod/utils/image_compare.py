__author__ = ""
__email__ = ""
__phone__ = ""
__license__ = "xxx"
__version__ = "1.0.0"
__maintainer__ = ""
__status__ = "Dev"

# Compares images in folder //AISMORGTK01/GELPhotos with image where camera is at pan 0
# puts all similar images in AISMORLAG01 c:\\gate_end_lag\scripts\filtered

import tensorflow as tf
from tensorflow import keras
import numpy as np

from prod import VariableClass
from prod.config_parser import config_json_parser

configs = config_json_parser()

file_type = configs[1]
filtered = configs[8]


def img_compare():
    # loads the model from the file name and creates a list of class names
    model = keras.models.load_model(r"C:\Users\ben.hamilton\PycharmProjects\Anglo\prod\utils\first_model.h5")
    class_names = ['badphotos', 'goodphotos']

    # takes the file path of the image being compared.
    # the script to find newly available photos and comparing them should most likely go here.
    sunflower_path = VariableClass.get_latest_image(filtered, file_type)
    img_name = sunflower_path[1]

    img = tf.keras.utils.load_img(
        img_name, target_size=(270, 480)
    )
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create a batch

    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    # prints out whether the image is good or not.
    # whether the image is good or not is stored in class_names[np.argmax(score).
    print(
        "This image most likely belongs to {} with a {:.2f} percent confidence."
            .format(class_names[np.argmax(score)], 100 * np.max(score))
    )


def main():
    img_compare()

