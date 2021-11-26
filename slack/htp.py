"""
Drew Dahlquist,
University of Missouri - Columbia,
College of Engineering,
Dept. of EECS

DMC Lab

2021
"""

from os import listdir
from os.path import abspath, getctime, join, isdir, isfile
from datetime import datetime
import psutil


def check_process_status(processName: str):
    """
    Check if there is any running process that contains the given name processName
    """

    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if(processName.lower() == proc.name().lower()):
                return True
        except(psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return False


def get_exp_info(experiment_directory: str):
    """
    Get information about experiment we want to report on in status update message
    Returns experiment name, and list of: most-recent photo names, their paths, and their times
    """

    # things we will return
    pic_rel_paths = list()
    pic_abs_paths = list()
    pic_times = list()

    # get abs path of top level dir we want to search
    topd_abs_path = abspath(experiment_directory)

    # get most recent experiment's dir
    sub_dirs = [subd for subd in listdir(
        topd_abs_path) if isdir(join(topd_abs_path, subd))]
    subd_rel_path = sorted(sub_dirs, key=lambda d: getctime(
        join(topd_abs_path, d)), reverse=True)[0]
    subd_abs_path = join(topd_abs_path, subd_rel_path)

    # get list of all position directories
    posd_rel_paths = [posd for posd in listdir(
        subd_abs_path) if isdir(join(subd_abs_path, posd))]
    posd_abs_paths = [join(subd_abs_path, posd) for posd in posd_rel_paths]

    # for all position dirs
    for posd in posd_abs_paths:
        # get pic & info
        pics = [pic for pic in listdir(posd) if (
            isfile(join(posd, pic)) and not pic.startswith('.'))]
        pic_rel_path = sorted(pics, key=lambda p: getctime(
            join(posd, p)), reverse=True)[0]
        pic_abs_path = join(posd, pic_rel_path)
        pic_time = datetime.fromtimestamp(
            getctime(pic_abs_path)).strftime('%Y-%m-%d %H:%M:%S')
        # appending to lists we'll return
        pic_rel_paths.append(pic_rel_path)
        pic_abs_paths.append(pic_abs_path)
        pic_times.append(pic_time)

    return subd_rel_path, pic_rel_paths, pic_abs_paths, pic_times


def get_dormant_count():
    """
    Get count (from text file) of how many consecutive "Dormant" messages we've sent
    """

    # work with file
    try:
        f = open("counter.txt", "r+")

        # get value in file
        contents = f.read()
        value = int(contents)

    # file was not found
    except FileNotFoundError:
        f = open("counter.txt", "w+")  # create file
        f.write("0")  # restart our count
        value = 0

    return value


def set_dormant_count(new_val: int):
    """
    Set count (in text file) of how many consecutive "Dormant" messages we've sent
    """

    # work with file
    try:
        f = open("counter.txt", "r+")  # open file that exists

        # update value in file
        f.seek(0)
        f.truncate()
        f.write(str(new_val))

    # file was not found
    except FileNotFoundError:
        f = open("counter.txt", "w+")  # create file
        f.write(str(new_val))  # set value
