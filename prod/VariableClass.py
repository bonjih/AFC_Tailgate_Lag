__author__ = ""
__email__ = ""
__phone__ = ""
__license__ = "xxx"
__version__ = "1.0.0"
__maintainer__ = ""
__status__ = "Dev"

import glob
import os
import pathlib
import time
from datetime import datetime
from PIL import Image  # count pixels

from prod import global_conf_variables

values = global_conf_variables.get_values()

GELPhotos = values[0]  # image from GelPhotos folder
file_type = values[1]
filtered = values[2]  # image for processing CV


class ImageData:
    """holds all database variables
      values sent to the db_manager and then the db

      Variables:
          date_time_db[0]  - date/time image added to db
          file_name[1]  - image name
          file_size[2]  - image file_size (on disk)
          num_pixels[3]  - image number of pixels
          date_time_create[4]  - date/time image was created (take by camera)
          image_id[5]  - id of image
          distance_lag[6] - tailgate distance from chain_dist_to_gate in mm
          chain_dist_to_gate[7] - chain_dist_to_gate in pixels
          cam_dist_to_gate[8] - distance in mm from bottom of image (camera) to tailgate (reference obj xA,yA)
          tailgate_coord_x[10] - tailgate_coord_x in image
          tailgate_coord_y[11] - tailgate_coord_y in image
          """

    def __init__(self, date_time_db, cam_dist_to_gate, chain_dist_to_gate, tailgate_coord_x, tailgate_coord_y,
                 distance_lead, distance_lag, file_size, file_name, num_pixels, date_time_create, image_id):
        self.date_time_db, self.cam_dist_to_gate, self.chain_dist_to_gate, self.tailgate_coord_x, self.tailgate_coord_y, \
        self.distance_lead, self.distance_lag, self.file_size, self.file_name, self.num_pixels, self.date_time_create, \
        self.image_id = date_time_db, cam_dist_to_gate, chain_dist_to_gate, tailgate_coord_x, tailgate_coord_y, \
                        distance_lead, distance_lag, file_size, file_name, num_pixels, date_time_create, image_id


# formats variables before sending to db_manager.py
def format_image_data(image_data):
    var = (ImageData(image_data[0], image_data[8], image_data[7], image_data[10],
                     image_data[11], image_data[7], image_data[6], image_data[2],
                     image_data[1], image_data[3], image_data[4], image_data[5]))

    return var.date_time_db, var.cam_dist_to_gate, var.chain_dist_to_gate, var.tailgate_coord_x, var.tailgate_coord_y, \
           var.distance_lead, var.distance_lag, var.file_size, var.file_name, var.num_pixels, var.date_time_create, \
           var.image_id


def file_type_check():
    list_of_files = glob.glob('./*')
    result = tuple(os.path.splitext(list_of_files[0]))
    result2 = '.' + file_type
    if result2 != result[1]:
        return False
    else:
        return True


def file_path_check():
    if filtered != filtered:  # path to image for processing in jconfig.json
        return False
    else:
        return True


#  gets the most recent image added to the directory
def get_latest_image(image_path, file_type):
    os.chdir(image_path)
    result = file_type_check()
    if result is True:
        list_of_files = glob.glob('./*.{}'.format(file_type))
        latest_file = max(list_of_files, key=os.path.getctime)
        file_name = latest_file[2:]
        image_id = file_name[:-4]
        return image_id, file_name
    else:
        pass


def img_meta_data():
    result = file_path_check()

    if result is True:
        path_to_img = pathlib.Path(filtered)  # change path to images in config.json 'filtered'
        # assert path_to_img.exists(), f'No such file: {path_to_img}'  # check that the file exists

        # date/time - when the  image is added to the database
        now = datetime.now()
        date_time_db = now.strftime('%Y-%m-%d %H:%M:%S')

        # date/time - when the image was created
        time_crt_str = (time.ctime(os.path.getmtime(path_to_img)))
        datetime_object_create = datetime.strptime(time_crt_str, "%a %b %d %H:%M:%S %Y")
        date_time_create = (datetime_object_create.strftime('%Y-%m-%d %H:%M:%S'))

        # file name and ID
        image_id, file_name = get_latest_image(filtered, file_type)

        # file size
        f_size = './{}'.format(file_name)
        file_size = os.path.getsize(f_size)

        # no of pixels
        width, height = Image.open(file_name).size
        num_pixels = width * height

        return date_time_db, file_name, file_size, num_pixels, date_time_create, image_id
    else:
        pass
