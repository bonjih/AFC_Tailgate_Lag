__author__ = "Ben Hamilton - Titan ICT Consultants"
__email__ = "ben.hamilton@titanict.com.au"
__phone__ = "+61 7 3360 4900"
__license__ = "xxx"
__version__ = "1.0.0"
__maintainer__ = "Anglo American"
__status__ = "Dev"

import glob
import os
import pathlib
import time
from datetime import datetime
from PIL import Image  # count pixels


class ImageData:
    """holds all database variables
      values sent to the db_manager and then the db

      Variables:
          date_time_db[0]  - date/time image added to db
          cam_dist_to_gate[17] - distance in mm from bottom of image (camera) to tailgate (reference obj xB,yB)
          chain_dist_to_gate[16] - chain_dist_to_gate in pixels
          tailgate_coord_x[37] - tailgate_coord_x in image
          tailgate_coord_y[38] - tailgate_coord_y in image
          distance_lead[16] - tailgate distance leading the pan
          distance_lag[15] - tailgate distance_lag
          file_size[2]  - image file_size (on disk)
          file_name[1]  - image name
          num_pixels[3]  - image number of pixels
          date_time_create[4]  - date/time image was created (take by camera)
          image_id[5]  - id of image"""

    def __init__(self, date_time_db, cam_dist_to_gate, chain_dist_to_gate, tailgate_coord_x, tailgate_coord_y,
                 distance_lead, distance_lag, file_size, file_name, num_pixels, date_time_create, image_id):
        self.date_time_db, self.cam_dist_to_gate, self.chain_dist_to_gate, self.tailgate_coord_x, self.tailgate_coord_y, \
        self.distance_lead, self.distance_lag, self.file_size, self.file_name, self.num_pixels, self.date_time_create, \
        self.image_id = date_time_db, cam_dist_to_gate, chain_dist_to_gate, tailgate_coord_x, tailgate_coord_y, \
                        distance_lead, distance_lag, file_size, file_name, num_pixels, date_time_create, image_id


# formats variable to for processing the db
def format_image_data(image_data):
    var = (ImageData(image_data[0], image_data[17], image_data[16], image_data[37],
                     image_data[38], image_data[16], image_data[15], image_data[2],
                     image_data[1], image_data[3], image_data[4], image_data[5]))

    return var.date_time_db, var.cam_dist_to_gate, var.chain_dist_to_gate, var.tailgate_coord_x, var.tailgate_coord_y, \
           var.distance_lead, var.distance_lag, var.file_size, var.file_name, var.num_pixels, var.date_time_create, \
           var.image_id


def img_meta_data(configs):
    image_path = configs[8]
    file_type = configs[1]

    # define file location .... may not need in fine solution
    path_to_img = pathlib.Path(image_path)  # change path to image in config.ini
    # assert f_name.exists(), f'No such file: {f_name}'  # check that the file exists

    # date/time - when the  image is added to the database
    now = datetime.now()
    date_time_db = now.strftime('%Y-%m-%d %H:%M:%S')

    # date/time - when the image was created
    time_crt_str = (time.ctime(os.path.getmtime(path_to_img)))
    datetime_object_create = datetime.strptime(time_crt_str, "%a %b %d %H:%M:%S %Y")
    date_time_create = (datetime_object_create.strftime('%Y-%m-%d %H:%M:%S'))

    # file name
    os.chdir(image_path)
    list_of_files = glob.glob('./*.{}'.format(file_type))
    latest_file = max(list_of_files, key=os.path.getctime)  # gets the most recent image added to the directory
    file_name = latest_file[2:]
    image_id = file_name[:-4]

    # file size
    f_path = './{}'.format(file_name)
    file_size = os.path.getsize(f_path)

    # no of pixels
    width, height = Image.open(file_name).size
    num_pixels = width * height

    return date_time_db, file_name, file_size, num_pixels, date_time_create, image_id
