from copy import copy
import json
import os


class FaceDatabase(object):
    def __init__(self, file_name):
        self._file_name = file_name
        self._faces = []
        
        if os.path.exists(self._file_name):
            with open(self._file_name, 'rb') as file_handler:
                self._faces = json.load(file_handler)

    @property
    def faces(self):
        return copy(self._faces)

    def add_face(self, face):
        self._faces.append(face)
        with open(self._file_name, 'wb') as file_handler:
            json.dump(file_handler, self._faces)
