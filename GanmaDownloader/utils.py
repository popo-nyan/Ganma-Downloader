import os


def make_directory(directory_name):
    if os.path.exists(directory_name):
        return
    else:
        os.mkdir(directory_name)

