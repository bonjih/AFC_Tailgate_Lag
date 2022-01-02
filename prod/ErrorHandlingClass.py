__author__ = ""
__email__ = ""
__phone__ = ""
__license__ = "xxx"
__version__ = "1.0.0"
__maintainer__ = ""
__status__ = "Dev"

import time
import pymysql as pymysql  # to catch db errors
from sqlalchemy import exc  # to catch db insert errors
import sqlalchemy  # to catch db insert errors
import shutil

# controls the error message sent interval in seconds
alarm_delay = 5


class ErrorMessageHandler:
    """ Error messages"""

    def __init__(self, error):
        try:
            raise error
        except FileNotFoundError as error:
            print("Can not reach 'jconfig.json' or path to image, please check path to image or config.json: {}".format(
                error))
            time.sleep(alarm_delay)
        except ValueError as error:
            print("Error in 'jconfig.json' format or cannot find an image or extension is incorrect or no file in dir "
                  "'filtered'. Please check config.json and dir 'filtered: {}".format(error))
            time.sleep(alarm_delay)
        except AttributeError as error:
            print('Error: {}'.format(error))
            time.sleep(alarm_delay)
        except TypeError as error:
            print("Error: {}".format(error))
            time.sleep(alarm_delay)
        except pymysql.OperationalError as error:
            print('No connection to database. Please check connection details in config.json: {}'.format(error))
            time.sleep(alarm_delay)
        except KeyboardInterrupt:
            print('\n! Received interrupt, quitting threads, restart main.py, check path to image in config.json.\n')
        except ConnectionResetError as error:
            print("Database connection restarted. Error: {}".format(error))
        except sqlalchemy.exc.OperationalError:
            print("There is a mismatch between table names in db_fields.json and the database.")
        except PermissionError as error:
            print("Read/Write: {}".format(error))
        except shutil.SameFileError as error:
            print("Some Err: {}".format(error))
