import os
import yaml


class ConfigHandler:
    def __init__(self, filename):
        self.filename = filename

    def load_yaml_file(self):
        with open(self.get_file_path(), "r") as f:
            return yaml.safe_load(f)

    def get_file_path(self):
        return os.path.join(os.path.dirname(__file__), self.filename)
