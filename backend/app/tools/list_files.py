import os


def list_files(directory="workspace"):

    if not os.path.exists(directory):
        return []

    return os.listdir(directory)