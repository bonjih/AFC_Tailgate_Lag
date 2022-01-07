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

from prod import VariableClass
from prod import LoggerClass

image_data = VariableClass.img_meta_data()


# controls the error message sent interval in seconds
alarm_delay = 5


class ErrorMessageHandler:
    """ Error messages """

    def __init__(self, error):

        try:
            raise error
        except FileNotFoundError as error:
            log_processing("Can not reach 'jconfig.json' or path to image: {}".format(error))
            time.sleep(alarm_delay)
        except ValueError as error:
            log_processing("Error in 'jconfig.json' format or cannot find an image or extension is incorrect, or no "
                           "file in dir 'filtered'. Check config.json and dir 'filtered: {}".format(error))
            time.sleep(alarm_delay)
        except AttributeError as error:
            log_processing('Error: {}'.format(error))
            time.sleep(alarm_delay)
        except TypeError as error:
            log_processing("Usually means image {} lacks detail for processing. Error: {}".format(image_data[1], error))
            time.sleep(alarm_delay)
        except pymysql.OperationalError as error:
            log_processing('No connection to database. Check connection details in config.json: {}'.format(error))
            time.sleep(alarm_delay)
        except KeyboardInterrupt:
            log_processing('\n! Received interrupt, quitting threads, restart main.py, check path to image in '
                           'jconfig.json.\n')
        except ConnectionResetError as error:
            log_processing("Database connection restarted. Error: {}".format(error))
        except sqlalchemy.exc.OperationalError:
            log_processing("There is a mismatch between table names in db_fields.json and the database.")
        except PermissionError as error:
            log_processing("Read/Write: {}".format(error))
        except shutil.SameFileError as error:
            log_processing("Some Err: {}".format(error))
        except OSError as error:
            log_processing("Can't access the Gelphotos directory: {}".format(error))
        except Exception as error:
            log_processing("Catch all error and log in [./log]: {}".format(error))


def log_processing(message):
    s = LoggerClass.ErrorLog(message)
    s.show()
