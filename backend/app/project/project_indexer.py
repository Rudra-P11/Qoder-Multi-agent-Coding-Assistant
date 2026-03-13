import os

class ProjectIndexer:

    def index_workspace(self, root="workspace"):

        tree = {}

        for root_dir, dirs, files in os.walk(root):

            tree[root_dir] = files

        return tree

project_indexer = ProjectIndexer()