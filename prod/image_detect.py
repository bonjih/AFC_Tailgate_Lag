__author__ = "Ben Hamilton - Titan ICT Consultants"
__email__ = "ben.hamilton@titanict.com.au"
__phone__ = "+61 7 3360 4900"
__license__ = "xxx"
__version__ = "1.0.0"
__maintainer__ = "Anglo American"
__status__ = "Dev"

import _thread
import glob
import os
import os.path
import pathlib
import threading
import time
from datetime import datetime

from PIL import Image  # count pixels
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

alarm_delay = 5


# global only used for configs in config.ini, in event_handler() and img_meta_data()
# retrieve image metadata
def img_meta_data(configs):
    global image_path, file_type  # change path/type in config.json
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


def on_created(event):
    print(f"{event.src_path} has been added to the directory")


# watchdog_timer() / watchdog_run(), to break the watchdog event_handler() While loop thread
def watchdog_timer(state):
    time.sleep(0.5)  # wait 0.5 seconds before breaking the event_handler() thread, then store image metadata as tuples
    if not state['completed']:
        _thread.interrupt_main()


def watchdog_run():
    while True:
        state = {'completed': False}
        watchdog = threading.Thread(target=watchdog_timer, args=(state,))
        watchdog.daemon = True
        watchdog.start()
        try:
            event_handler()
            state['completed'] = True
        except KeyboardInterrupt:
            print('\n! Received interrupt, quitting threads, restart main.py.\n')
        except FileNotFoundError as e:
            print("Can not reach path image, please check path to image in config.json: {}".format(e))
            time.sleep(alarm_delay)

            pass
        else:
            break


# main event handler, calls on_created() to notify when a file is added to the dir
def event_handler():
    patterns = ["*.{}".format(file_type)]  # from global, change file type in config.json
    ignore_patterns = None
    ignore_directories = True
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
    my_event_handler.on_created = on_created
    path = image_path  # from global, path to image for watchdog, change in config.ini
    go_recursively = True
    file_observer = Observer()
    file_observer.schedule(my_event_handler, path, recursive=go_recursively)
    file_observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        file_observer.stop()
    file_observer.join()
