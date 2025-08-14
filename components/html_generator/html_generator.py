import os
from typing import Any

from utils import load_yaml


class HTMLGenerator:
    """
    Base class for generating HTML pages.
    """
    def __init__(self, output_dir: str, output_file_name: str, config_path: str):
        """
        HTMLGenerator constructor.
        :param output_dir: path to output directory
        :param output_file_name: output file name
        :param config_path: path to config file
        """
        self.config = load_yaml(config_path)
        self.output_dir = output_dir
        self.output_file_name = output_file_name

    def save_file(self, html: str) -> str:
        """
        save html to file.
        :param html:
        :return:
        """
        file_path = os.path.join(self.output_dir, f"{self.output_file_name}.html")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)

        return file_path

    def generate(self, data: Any) -> str:
        """
        abstract method for generating HTML pages logic
        :param data: data for the html page generation
        """
        raise NotImplementedError("This method must be implemented in subclass")

    def generate_and_save(self, data: Any) -> str:
        """
        generate and save the html page
        :param data: data for the html page generation
        :return: the html page file path
        """
        data = self.generate(data)
        file_path = self.save_file(data)
        return file_path

