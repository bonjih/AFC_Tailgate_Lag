__author__ = "Ben Hamilton - Titan ICT Consultants"
__email__ = "ben.hamilton@titanict.com.au"
__phone__ = "+61 7 3360 4900"
__license__ = "xxx"
__version__ = "1.0.0"
__maintainer__ = "Anglo American - email: "
__status__ = "Dev"


import image_detect
import db_manager
import cv_image_processing
import time
import json
import pymysql as pymysql  # to catch db errors
from sqlalchemy import exc  # to catch db insert errors
import sqlalchemy  # to catch db insert errors

# controls the error message sent interval in seconds
alarm_delay = 5


#############################################
# load jconfig.json
# if required, change variables in jconfig.json
#############################################
def config_json_parser():
    config_values = []

    with open(r'C:\Users\ben.hamilton\PycharmProjects\Anglo\config.json', 'r') as jsonFile:
        data = json.load(jsonFile)
        for key, value in data.items():
            config_values.append(value)
    return config_values


def db_json_parser():
    db_field_key = []

    with open(r'C:\Users\ben.hamilton\PycharmProjects\Anglo\db_fields.json', 'r') as jsonFile:
        data = json.load(jsonFile)
        for key, value in data.items():
            db_field_key.append(key)
    return db_field_key


def image_detect_controller():
    img_meta_data = image_detect.img_meta_data(jconfigs)
    image_detect.watchdog_run()
    return img_meta_data


# formats all variable to for processing the db
def format_image_data(img_data):
    cv_data_tup = cv_image_processing.cv_processing(img_data)

    cv_data = cv_data_tup[0] + cv_data_tup[1]  # concatenate cv_data list, pass to db_manager.image_data()
    img_meta_data = image_detect_controller()
    image_data = list(img_meta_data) + cv_data

    # values sent to the db_manager and then the db

    # image_data[0]  - date/time image added to dir
    # image_data[15] - distance in mm from bottom of image (camera) to tailgate (reference obj xA,xB)
    # image_data[20] - cam_dist_to_gate in pixels
    # image_data[35] - tailgate_coord_x in image
    # image_data[36] - tailgate_coord_y in image
    # image_data[16]  - tailgate distance leading the pan
    # image_data[9]  - tailgate distance_lag
    # image_data[2]  - image file_size (on disk)
    # image_data[1]  - image name
    # image_data[3]  - image number of pixels
    # image_data[4]  - date/time image was created (take by camera)
    # image_data[5]  - id of image

    image_data2 = (image_data[0], image_data[15], image_data[20], image_data[35], image_data[36], image_data[16],
                   image_data[9], image_data[2], image_data[1], image_data[3], image_data[4], image_data[5])

    return image_data2, img_meta_data


def db_manager_controller(dbfields):
    dir_img_name = image_detect.img_meta_data(jconfigs)
    db_manager.db_creds_json(jconfigs)
    db_manager.db_connect()

    exists = db_manager.check_entry_exist(dir_img_name)

    image_data2, img_meta_data = format_image_data(jconfigs)

    if not exists:
        db_manager.image_data(image_data2, dbfields)  # for a single db insert
    else:
        print("latest image, '{}', already in the database, skipping....".format(img_meta_data[1]))


if __name__ == "__main__":
    # loop forever, waits for a new image

    while True:
        print('Checking for latest image.....')
        try:
            jconfigs = config_json_parser()
            image_detect_controller()
            cv_image_processing.load_image(jconfigs)
            db_fields = db_json_parser()
            db_manager_controller(db_fields)

        except FileNotFoundError as e:
            print("Can not reach 'jconfig.json' or path to image, please check path to image or config.json: {}".format(
                e))
            time.sleep(alarm_delay)
        except ValueError as e:
            print("Error in 'jconfig.json' format or cannot find an image or extension is incorrect. Please check "
                  "config.json: {}".format(e))
            time.sleep(alarm_delay)
        except AttributeError as e:
            print('Error: {}'.format(e))
            time.sleep(alarm_delay)
        except TypeError as e:
            print("Error: {}".format(e))
            time.sleep(alarm_delay)
        except pymysql.OperationalError as e:
            print('No connection to database. Please check connection details in config.json: {}'.format(e))
            time.sleep(alarm_delay)
        except KeyboardInterrupt:
            print('\n! Received interrupt, quitting threads, restart main.py, check path to image in config.json.\n')
        except ConnectionResetError as e:
            print("Database connection restarted. Error: {}".format(e))
        except sqlalchemy.exc.OperationalError as e:
            print("There is a mismatch between table names in db_fields.json and the database.")



