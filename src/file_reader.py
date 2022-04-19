#!/usr/bin/env python

"""This module stores path to files and reads them."""

import json
import os
from typing import TypeVar

FileReaderObject = TypeVar('FileReaderObject', bound='FileReader')


class FileReader:
    """
    This class holds the path to all the given files and their aliases, and reads those files.
    """

    __files: dict = None
    """Stores path to all files and aliases to their."""

    def __init__(self, associative_name: str = 'pins', path_to_file: str = '../data/pins.json') -> None:
        """
        This constructor writes path to one given file.
        
        :param associative_name: str | Key to FileReader dictionary
        :param path_to_file: str | Value to FileReader dictionary
        """
        self.__files = {}
        self.add_file(associative_name, path_to_file)

    def add_file(self, associative_name: str, path_to_file: str) -> FileReaderObject:
        """
        Writes a key and value to a FileReader dictionary and checks if the file exists.

        :param associative_name: str | Key to FileReader dictionary
        :param path_to_file: str | Value to FileReader dictionary
        :return: self
        """
        if not os.path.isfile(path_to_file):
            raise Exception('File "' + path_to_file + '" not found.')
        self.__files[associative_name] = path_to_file
        return self

    def del_file(self, associative_name: str) -> FileReaderObject:
        """
        Removes the file path from the FileReader dictionary.

        :param associative_name: str | Key to FileReader dictionary
        :return: self
        """
        del self.__files[associative_name]
        return self

    def get_files_dictionary(self) -> dict:
        """
        Returns a dictionary of files.

        :return: dict | File dictionary
        """
        return self.__files.copy()

    def show_files(self) -> FileReaderObject:
        """
        Shows all keys and values that are stores.

        :return: self
        """
        for key, value in self.__files.items():
            print(key + ' : ' + value)
        return self

    def get_data(self, associative_name: str) -> dict:
        """
        Retrieves all data from a file.

        :param associative_name: str | Key to FileReader dictionary
        :return: dict | All data from file
        """
        file = open(self.__files[associative_name], 'r')
        data = json.load(file)
        file.close()
        return data
