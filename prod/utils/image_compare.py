__author__ = ""
__email__ = ""
__phone__ = ""
__license__ = "xxx"
__version__ = "1.0.0"
__maintainer__ = ""
__status__ = "Dev"

# Compares images in folder //AISMORGTK01/GELPhotos with image where camera is at pan 0
# puts all similar images in AISMORLAG01 c:\gate_end_lag\scripts\utils\filtered

import os
import tensorflow as tf
from tensorflow import keras
import numpy as np
import shutil

from prod import VariableClass, global_conf_variables, cv_image_processing
from prod.config_parser import config_json_parser

config = config_json_parser()

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

values = global_conf_variables.get_values()

GELPhotos = values[0]  # image from GelPhotos folder
file_type = values[1]
filtered = values[2]  # image for processing CV


def img_skip_messsage():
    img_name = VariableClass.get_latest_image(GELPhotos, file_type)
    print('Skipping image [{}], does not meet quality standards'.format(img_name[1]))


def img_compare():
    # loads the model from the file name and creates a list of class names
    model = keras.models.load_model(r"C:\Users\ben.hamilton\PycharmProjects\Anglo\prod\utils\first_model.h5")
    class_names = ['bad_photos', 'good_photos']

    # takes the file path of the image being compared.
    # the script to find newly available photos and comparing them should most likely go here.

    sunflower_path = VariableClass.get_latest_image(GELPhotos, file_type)
    img_name = sunflower_path[1]

    img = tf.keras.utils.load_img(img_name, target_size=(270, 480))
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create a batch

    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])
    add_img_if = class_names[np.argmax(score)], 100 * np.max(score)

    result = cv_image_processing.cv_processing()
    if add_img_if[0] == 'good_photos' and result is True:
        shutil.copy('{}/{}'.format(GELPhotos, img_name), filtered)
    else:
        pass


def main():
    img_compare()
