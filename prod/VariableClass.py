__author__ = "Ben Hamilton - Titan ICT Consultants"
__email__ = "ben.hamilton@titanict.com.au"
__phone__ = "+61 7 3360 4900"
__license__ = "xxx"
__version__ = "1.0.0"
__maintainer__ = "Anglo American"
__status__ = "Dev"


class ImageData:
    """holds all database variables
      values sent to the db_manager and then the db

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
