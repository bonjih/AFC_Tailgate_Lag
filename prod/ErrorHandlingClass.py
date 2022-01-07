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
            s = LoggerClass.ErrorLog("Can not reach 'jconfig.json' or path to image: {}".format(
                error))
            s.show()
            time.sleep(alarm_delay)
        except ValueError as error:
            s = LoggerClass.ErrorLog(
                "Error in 'jconfig.json' format or cannot find an image or extension is incorrect, "
                "or no file in dir 'filtered'. Please check config.json and dir 'filtered: {}".format(
                    error))
            s.show()
            time.sleep(alarm_delay)
        except AttributeError as error:
            s = LoggerClass.ErrorLog('Error: {}'.format(error))
            time.sleep(alarm_delay)
            s.show()
        except TypeError as error:
            s = LoggerClass.ErrorLog(
                "Usually means image {} lacks detail for processing. Error: {}".format(image_data[1], error))
            s.show()
            time.sleep(alarm_delay)
        except pymysql.OperationalError as error:
            s = LoggerClass.ErrorLog(
                'No connection to database. Please check connection details in config.json: {}'.format(error))
            s.show()
            time.sleep(alarm_delay)
        except KeyboardInterrupt:
            s = LoggerClass.ErrorLog(
                '\n! Received interrupt, quitting threads, restart main.py, check path to image in config.json.\n')
            s.show()
        except ConnectionResetError as error:
            s = LoggerClass.ErrorLog("Database connection restarted. Error: {}".format(error))
            s.show()
        except sqlalchemy.exc.OperationalError:
            s = LoggerClass.ErrorLog("There is a mismatch between table names in db_fields.json and the database.")
            s.show()
        except PermissionError as error:
            s = LoggerClass.ErrorLog("Read/Write: {}".format(error))
            s.show()
        except shutil.SameFileError as error:
            s = LoggerClass.ErrorLog("Some Err: {}".format(error))
            s.show()
        except OSError as error:
            s = LoggerClass.ErrorLog("Can't access the Gelphotos directory: {}".format(error))
            s.show()
        except Exception as error:
            s = LoggerClass.ErrorLog("Catch all error and log in [./log]: {}".format(error))
            s.show()
