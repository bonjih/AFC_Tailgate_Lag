__author__ = ""
__email__ = ""
__phone__ = ""
__license__ = "xxx"
__version__ = "1.0.0"
__maintainer__ = ""
__status__ = "Dev"

import _thread
import threading
import time

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer
from prod.config_parser import config_json_parser

alarm_delay = 5

config = config_json_parser()
image_path = config[8]  # path to image for processing in jconfig
file_type = config[1]


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
    patterns = ["*.{}".format(file_type)]
    ignore_patterns = None
    ignore_directories = True
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
    my_event_handler.on_created = on_created
    go_recursively = True
    file_observer = Observer()
    file_observer.schedule(my_event_handler, image_path, recursive=go_recursively)
    file_observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        file_observer.stop()
    file_observer.join()
