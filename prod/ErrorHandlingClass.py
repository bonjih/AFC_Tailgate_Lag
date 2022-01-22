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

from prod import LoggerClass, global_conf_variables

# controls the error message sent interval in seconds
alarm_delay = 5

variables = global_conf_variables.GlobalVars

file_type = variables.file_type


class ErrorMessageHandler:
    """ Error messages """

    def __init__(self, error):

        try:
            raise error
        except KeyboardInterrupt:
            LoggerClass.log_processing('\n! Received interrupt, quitting threads, restart main.py, check path to image '
                                       'in jconfig.json.\n')
        except AttributeError as error:
            LoggerClass.log_processing('Error: {}'.format(error))
            time.sleep(alarm_delay)
        except FileNotFoundError as error:
            LoggerClass.log_processing("Can not reach 'jconfig.json' or path to image: {}".format(error))
            time.sleep(alarm_delay)
        except ValueError as error:

            LoggerClass.log_processing("Image: Error in 'jconfig.json' format or cannot find an image or extension is "
                                       "incorrect, or no file in dir 'filtered, or bad read image'. "
                                       "Check config.json and dir 'filtered: "
                                       "{}".format(error))
            time.sleep(alarm_delay)
        except TypeError as error:
            LoggerClass.log_processing("Check image extension matches extension in jconfigs.json, or could mean "
                                       "image lacks detail for processing. Error: {}".format(error))
            time.sleep(alarm_delay)
        except pymysql.OperationalError as error:
            LoggerClass.log_processing('No connection to database. Check connection details in config.json: {}'
                                       .format(error))
            time.sleep(alarm_delay)
        except ConnectionResetError as error:
            LoggerClass.log_processing("Database connection restarted. Error: {}".format(error))
        except sqlalchemy.exc.OperationalError:
            LoggerClass.log_processing("There is a mismatch between table names in db_fields.json and the database.")
        except PermissionError as error:
            LoggerClass.log_processing("Read/Write: {}".format(error))
        except shutil.SameFileError as error:
            LoggerClass.log_processing("Some Err: {}".format(error))
        except OSError as error:
            LoggerClass.log_processing("Can't access the Gelphotos or another directory, check error: {}".format(error))
            time.sleep(alarm_delay)
        except IndexError as error:
            LoggerClass.log_processing("Most likely no image in dir ./Gelphotos: {}".format(error))
            time.sleep(alarm_delay)
        except Exception as error:
            LoggerClass.log_processing("Catch all error and log in [./log]: {}".format(error))
            print(type(error))
            time.sleep(alarm_delay)

