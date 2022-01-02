__author__ = ""
__email__ = ""
__phone__ = ""
__license__ = "xxx"
__version__ = "1.0.0"
__maintainer__ = ""
__status__ = "Dev"

# Compares images in folder //AISMORGTK01/GELPhotos with image where camera is at pan 0
# puts all similar images in AISMORLAG01 c:\\gate_end_lag\scripts\filtered

import cv2 as cv
import random
import glob
import shutil
import os
import numpy as np

from prod import VariableClass

samples = r"C:\Users\ben.hamilton\PycharmProjects\Anglo\prod\utils\samples"


def dir_check():
    os.chdir(r'C:\Users\ben.hamilton\PycharmProjects\Anglo\prod\utils')
    samples_exists = os.path.isdir('samples')

    if samples_exists is True:
        for file in os.scandir(samples):
            os.remove(file.path)

    if samples_exists is False:
        os.mkdir("samples")


def rand_sample(configs):
    global file_type
    global filtered

    image_path = configs[0]
    file_type = configs[1]
    filtered = configs[8]

    os.chdir(image_path)
    list_of_files = glob.glob('./*.{}'.format(file_type))

    file_names = []
    for img in list_of_files:
        file_names.append(img[2:])

    len_dir = len(file_names)
    len_sample = round(len_dir / 2)
    rand_num = random.sample(range(len_dir), int(len_sample))

    for num in rand_num:
        shutil.copy(os.path.join(image_path, file_names[num]),
                    samples)


def template_match():
    template = cv.imread('template.jpg', 0)
    template = cv.blur(template, (8, 8))
    template = cv.dilate(template, ())
    h, w = template.shape[::]
    threshold = 0.535

    file_name = VariableClass.get_latest_image(samples, file_type)

    sampling = cv.imread(file_name[1], 0)
    sampling = cv.blur(sampling, (8, 8))
    res = cv.matchTemplate(sampling, template, cv.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)

    x = []
    for pt in zip(*loc[::-1]):
        x.append(pt[0])

    if len(x) != 0 and (max(x) - min(x)) < 100:
        # range = max(x) - min(x)
        # print(img, range)
        shutil.move(file_name, '{}/'.format(filtered))


def main(configs):
    dir_check()
    rand_sample(configs)
    template_match()

