import os


def get_files_in_testdir_by_extension(dir_name, extension):
    return [file for file in os.listdir(dir_name) if f".{extension}" in file]
