from copy import copy
import pickle
import os


class FaceDatabase(object):
    def __init__(self, file_name):
        self._file_name = file_name
        self._faces = {'named': [], 'unnamed': []}

        if os.path.exists(self._file_name):
            with open(self._file_name, 'rb') as file_handler:
                self._faces = pickle.load(file_handler)

        else:
            with open(self._file_name, 'wb') as file_handler:
                pickle.dump(self._faces, file_handler)

    @property
    def faces(self):
        return self.unnamed_faces + copy(self._faces['named'])

    @property
    def unnamed_faces(self):
        return copy(self._faces['unnamed'])

    def add_face(self, face):
        self._faces['unnamed'].append(face)
        with open(self._file_name, 'wb') as file_handler:
            pickle.dump(self._faces, file_handler)

    def __len__(self):
        return len(self._faces['named']) + len(self._faces['unnamed'])
