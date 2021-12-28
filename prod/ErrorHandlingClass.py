__author__ = "Ben Hamilton - Titan ICT Consultants"
__email__ = "ben.hamilton@titanict.com.au"
__phone__ = "+61 7 3360 4900"
__license__ = "xxx"
__version__ = "1.0.0"
__maintainer__ = "Anglo American"
__status__ = "Dev"

import time

# controls the error message sent interval in seconds
alarm_delay = 5


class ErrorMessageHandler:
    """ Error messages"""

    def __init__(self, error):
        err_type = str(type(error))
        err_type = (err_type[8:-2])

        if err_type == 'FileNotFoundError':
            print("Can not reach 'jconfig.json' or path to image, please check path to image or config.json: {}".format(
                    error))
            time.sleep(alarm_delay)

        elif err_type == 'ValueError':
            print("Can not reach 'jconfig.json' or path to image, please check path to image or config.json: {}".format(
                error))
            time.sleep(alarm_delay)

        elif err_type == 'AttributeError':
            print('Error: {}'.format(error))
            time.sleep(alarm_delay)

        elif err_type == 'TypeError':
            print('Error: {}'.format(error))
            time.sleep(alarm_delay)

        elif err_type == 'pymysql.OperationalError':
            print('No connection to database. Please check connection details in config.json: {}'.format(error))
            time.sleep(alarm_delay)

        elif err_type == 'KeyboardInterrupt':
            print('\n! Received interrupt, quitting threads, restart main.py, check path to image in config.json.\n')
            time.sleep(alarm_delay)

        elif err_type == 'ConnectionResetError':
            print("Database connection restarted. Error: {}".format(error))
            time.sleep(alarm_delay)

        elif err_type == 'sqlalchemy.exc.OperationalError':
            print("There is a mismatch between table names in db_fields.json and the database.")
            time.sleep(alarm_delay)

        elif err_type == 'PermissionError':
            print("Read/Write: {}".format(error))
            time.sleep(alarm_delay)

        elif err_type == 'shutil.SameFileError':
            print("Some Error with 'image_compare.py': {}".format(error))
            time.sleep(alarm_delay)

        elif err_type == 'shutil.Error':
            print("Some Error with 'image_compare.py': {}".format(error))
            time.sleep(alarm_delay)
