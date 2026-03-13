import os


def search_code(query: str):

    results = []

    for root, _, files in os.walk("workspace"):

        for file in files:

            path = os.path.join(root, file)

            with open(path, "r", errors="ignore") as f:

                if query in f.read():

                    results.append(path)

    return results