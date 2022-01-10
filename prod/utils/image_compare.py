__author__ = ""
__email__ = ""
__phone__ = ""
__license__ = "xxx"
__version__ = "1.0.0"
__maintainer__ = ""
__status__ = "Dev"

# Compares images in folder //AISMORGTK01/GELPhotos with image where camera is at pan 0
# puts all similar images in AISMORLAG01 c:\\gate_end_lag\scripts\filtered
import os
import tensorflow as tf

from tensorflow import keras
import numpy as np
import shutil

from prod import VariableClass
from prod.config_parser import config_json_parser

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

config = config_json_parser()

GELPhotos = config[0]  # image from GelPhotos folder
file_type = config[1]
filtered = config[8]


def img_compare():
    # loads the model from the file name and creates a list of class names
    model = keras.models.load_model(r"C:\Users\ben.hamilton\PycharmProjects\Anglo\prod\utils\first_model.h5")
    class_names = ['badphotos', 'goodphotos']

    # takes the file path of the image being compared.
    # the script to find newly available photos and comparing them should most likely go here.

    sunflower_path = VariableClass.get_latest_image(GELPhotos, file_type)
    img_name = sunflower_path[1]

    img = tf.keras.utils.load_img(
        img_name, target_size=(270, 480)
    )
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create a batch

    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])
    add_img_if = class_names[np.argmax(score)], 100 * np.max(score)
    if add_img_if[0] == 'goodphotos':
        shutil.copy(GELPhotos + '/' + img_name, filtered)
    else:
        print('Skipping image [{}], does not meet quality standards'.format(img_name))

    # prints out whether the image is good or not.
    # whether the image is good or not is stored in class_names[np.argmax(score).
    # print(
    #     "This image most likely belongs to {} with a {:.2f} percent confidence."
    #         .format(class_names[np.argmax(score)], 100 * np.max(score))
    # )


def main():
    img_compare()
