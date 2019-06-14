from abc import ABCMeta
import pickle
import json
import os


class Database(object):
    __metaclass__ = ABCMeta

    def __init__(self, file_name, initial_data=[], serialization_type='pickle'):
        self._file_name = file_name
        self._data = initial_data

        if serialization_type == 'pickle':
            self._serialization_module = pickle

        elif serialization_type == 'json':
            self._serialization_module = json

        if os.path.exists(self._file_name):
            self._read_data()
        else:
            self._write_data()

    def _write_data(self):
        with open(self._file_name, 'wb') as file_handler:
            self._serialization_module.dump(self._data, file_handler)

    def _read_data(self):
        with open(self._file_name, 'rb') as file_handler:
            self._data = self._serialization_module.load(file_handler)

    def __len__(self):
        self._read_data()
        return len(self._data)

    def __getitem__(self, item):
        """
        return an item by his id
        :param item: id/s of an object/s in the database
        :return: the object/s
        """
        self._read_data()

        if type(item) is int:
            return self._data[item]

        elif type(item) is list:
            return [self._data[index] for index in item]

    def __delitem__(self, key):
        self._read_data()
        self._data[key] = None
        self._write_data()
