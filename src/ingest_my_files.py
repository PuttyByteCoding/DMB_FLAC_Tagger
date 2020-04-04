import os
from loguru import logger
import requests
import json
import shutil
import re

def add_concert_dir_to_database(show_dict):
    session = requests.Session()
    request = session.post(f'http://localhost:8000/concert_dir/',
                           headers={
                               'Content-type': 'application/json',
                               'Accept': 'text/plain'},
                           data=json.dumps(show_dict))
    if request.status_code == 200:
        return True
    else:
        return False


def start_ingest():
    ORIGINALS_DIR = "/Volumes/500GB_SSD/01-originals"
    READY_TO_TAG_DIR = "/Volumes/500GB_SSD/02-ready_to_tag"

    processed_directories = 0
    directories_list = directories_gen(ORIGINALS_DIR)
    for show_dir in directories_list:
        processed_directories += 1
        show_dir_entry = {}
        logger.info(f"Processing show {processed_directories} of {len(directories_list)} in directory: {show_dir}")
        parent_dir, show_dir_name = os.path.split(show_dir)

        # Copy files to READY_TO_TAG
        source_dir = show_dir
        destination_dir = os.path.join(READY_TO_TAG_DIR, show_dir_name)
        show_dir_entry['local_path'] = destination_dir
        show_dir_entry['web_path'] = os.path.join("/", show_dir_name)
        if os.path.isdir(destination_dir):
            logger.warning(f"{destination_dir} already exists.  Skipping copy.")
        else:
            shutil.copytree(source_dir, destination_dir)

        # Flatten Directory
        for f in filelist_gen(destination_dir):
            f_dir, f_name = os.path.split(f)
            if f_dir == destination_dir:
                pass
            else:
                relative_path = os.path.relpath(f, destination_dir)
                flattened_filename = relative_path.replace("/", "_")
                flattened_file_dest_path = os.path.join(destination_dir, flattened_filename)
                shutil.move(f, flattened_file_dest_path)

        # Determine concert date and band configuration
        pattern = re.compile('\d\d\d\d-\d\d-\d\d')
        matches = pattern.findall(show_dir_name)
        if len(matches) == 1:
            show_dir_entry['date_from_directory_name'] = matches[0]
            date_start_offset = pattern.search(show_dir_name).start()
            show_dir_entry['band_configuration_from_directory_name'] = show_dir_name[0:date_start_offset].lower()
        else:
            show_dir_entry['date_from_directory_name'] = "Unable To Determine"
            show_dir_entry['band_configuration_from_directory_name'] = "Unable To Determine"

        add_concert_dir_to_database(show_dir_entry)


def create_dir_if_doesnt_exist(path):
    if os.path.isdir(path):
        pass
    else:
        os.makedirs(path)
    return


def directories_gen(root_dir):
    logger.info("Starting: Creating list of show directories")
    dirs_path_list = []
    for root, dirs, files in os.walk(root_dir):
        for directory in dirs:
            path = os.path.join(root, directory)
            dirs_path_list.append(path)
        break # prevents recursion
    logger.info("Finished: Creating list of directories")
    return dirs_path_list


def flac_filelist_gen(root_dir):
    logger.info("Starting: Creating list of FLAC files")
    files_path_list = []
    for root, dirs, files in os.walk(root_dir):
        for name in files:
            path = os.path.join(root, name)
            if os.path.islink(path):
                pass
            else:
                if path[-5:].lower() == ".flac":
                    files_path_list.append(path)
    logger.info("Finished: Creating list of files")
    return files_path_list


def filelist_gen(root_dir):
    logger.info("Starting: Creating list of files")
    for root, dirs, files in os.walk(root_dir):
        for name in files:
            path = os.path.join(root, name)
            if os.path.islink(path):
                pass
            else:
                yield path
    return


if __name__ == "__main__":
    start_ingest()
