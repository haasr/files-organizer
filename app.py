from config import *

import multiprocessing
import logging
import shutil
import os

from sys import platform
from time import sleep

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


observer = Observer()


logging.basicConfig(level=LOG_LEVEL,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S,',
                    filename=LOG_FILE_PATH,
                    filemode=LOG_FILE_MODE)

logger = logging.getLogger(__name__)


# make_unique and move_file based on https://github.com/tuomaskivioja/File-Downloads-Automator/blob/main/fileAutomator.py
def make_unique(dest, name):
    filename, extension = os.path.splitext(name)
    counter = 1
    while os.path.exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        logger.info(f"Renamed file to {name}")
        counter += 1

    return name


def move_file(source_dir, dest, filename):
    global logger
    sleep(2)
    dest_name = make_unique(dest, filename)
    # Stopped using os.path.join -- uses backlashes in Windows which don't mix with the forward slashes. 
    try:
        if filename != dest_name:
            os.rename(f"{dest}/{filename}", f"{dest}/{dest_name}")
        
        source_path = f"{source_dir}/{dest_name}"
        dest_path = f"{dest}/{dest_name}"
        logger.info(f"Moving file {source_path} to {dest_path} ...")
        shutil.move(source_path, dest_path)
    except Exception as e:
        logger.exception(e) # Could cause an exception if the user moves the file at just the perfect (wrong) time...


class FileMover(FileSystemEventHandler):
    global logger
    def __init__(self, source_dir):
        self.source_dir = source_dir # The directory to monitor
        self.source_ext_categories = DIRECTORIES_MAP[source_dir] # The categories to look for in this directory
        logger.info(f"Listening to {source_dir} ...")


    def check_ext(self, filename):
        ext = os.path.splitext(filename)[1].lower()

        for category in self.source_ext_categories:
            if ext in EXTENSIONS_MAP[category]:
                logger.info(f"New or modified \"{category}\" file detected: {filename}")
                move_file(self.source_dir, dest=DIRECTORIES_MAP[self.source_dir][category],
                            filename=filename)
                break


    def on_modified(self, event):
        for root, dirs, files in os.walk(self.source_dir, topdown=True): # Topdown keeps it in parent dir
            dirs.clear() # Skip em
            for filename in files:
                self.check_ext(filename)


def monitor_dir(event_handler, dir):
    global observer

    observer.start()
    observer.schedule(event_handler, dir, recursive=OBSERVER_RECURSIVE)
    try:
        while True:
            sleep(15)
    except KeyboardInterrupt:
        logger.info("Interrupt received. Exiting...")
        observer.stop()
        logger.info("Observer exited")
    observer.join()


def try_create_folders():
    for dir in DIRECTORIES_MAP.keys():
        for category in DIRECTORIES_MAP[dir]:
            try: os.makedirs(DIRECTORIES_MAP[dir][category])
            except: pass # Already exists (or bad write permission)


if __name__ == "__main__":
    try_create_folders()

    # Set process start method to spawn if MacOS or Windows:
    if ( platform.startswith('win') or platform.startswith('cygwin') or platform.startswith('darwin') ):
        multiprocessing.set_start_method('spawn')

    for source_dir in DIRECTORIES_MAP.keys():
        event_handler = FileMover(source_dir=source_dir)
        p = multiprocessing.Process(target=monitor_dir, args=(event_handler, source_dir))
        p.start()