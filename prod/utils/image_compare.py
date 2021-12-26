__author__ = "Ben Hamilton - Titan ICT Consultants"
__email__ = "ben.hamilton@titanict.com.au"
__phone__ = "+61 7 3360 4900"
__license__ = "xxx"
__version__ = "1.0.0"
__maintainer__ = "Anglo American - email: "
__status__ = "Dev"

# Compares images in folder //AISMORGTK01/GELPhotos with image where camera is at pan 0
# puts all similar images in AISMORLAG01\\gate_end_lag\scripts\filtered

import cv2 as cv
import random
import glob
import shutil
from sewar.full_ref import scc
from skimage import metrics
import os
import numpy as np


def rand_sample():
    shutil.rmtree("samples")
    shutil.rmtree("filtered")
    os.mkdir("samples")
    os.mkdir("filtered")

    file_names = []
    for img in glob.glob('GelPhotos/*'):
        file_names.append(img)

    len_dir = len(file_names)

    rand_num = random.sample(range(len_dir), 50)

    for num in rand_num:
        shutil.copy(file_names[num], "samples/")


def template_match():
    template = cv.imread('template.jpg', 0)
    template = cv.blur(template, (8, 8))
    template = cv.dilate(template, ())
    h, w = template.shape[::]
    threshold = 0.535

    for img in glob.glob('samples/*'):
        sampleimg = cv.imread(img, 0)
        sampleimg = cv.blur(sampleimg, (8, 8))
        res = cv.matchTemplate(sampleimg, template, cv.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)

        x = []
        for pt in zip(*loc[::-1]):
            x.append(pt[0])

        if len(x) != 0 and (max(x) - min(x)) < 100:
            # range = max(x) - min(x)
            # print(img, range)
            shutil.move(img, 'filtered/')


if __name__ == "__main__":
    rand_sample()
    # template_match()
