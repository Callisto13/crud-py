import os

class Handlers:
    def __init__(self, store):
        self.store = store

    def create(self, name, contents):
        full_path = self.store+'/'+name
        if not os.path.exists(full_path):
            self.write_file(full_path, contents)
            return "File '{}' created at '{}'.".format(name, self.store), 201
        else:
            return "File '{}' already exists in '{}'.".format(name, self.store), 409

    def list(self):
        files = os.listdir(self.store)
        if len(files) == 0:
            return "No files found in {}".format(self.store)
        return '\n'.join(sorted(files))

    def read(self, name):
        full_path = self.store+'/'+name
        if os.path.exists(full_path):
            f = open(full_path, "r")
            contents = f.read()
            f.close()
            return contents
        else:
            return "File '{}' not found in '{}'.".format(name, self.store), 404

    def update(self, name, contents):
        full_path = self.store+'/'+name
        if os.path.exists(full_path):
            self.write_file(full_path, contents)
            return "File '{}' in '{}' updated.".format(name, self.store)
        else:
            return "File '{}' not found in '{}'.".format(name, self.store), 404

    def delete(self, name):
        full_path = self.store+'/'+name
        if os.path.exists(full_path):
            os.remove(full_path)
            return "File '{}' deleted from '{}'.".format(name, self.store)
        else:
            return "File '{}' not found in '{}'.".format(name, self.store), 404

    def write_file(self, filename, contents):
        f = open(filename, "w")
        f.write(contents)
        f.close()

