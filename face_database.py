from copy import copy
import pickle
import os


class FaceDatabase(object):
    def __init__(self, file_name):
        self._file_name = file_name
        self._faces = []

        if os.path.exists(self._file_name):
            with open(self._file_name, 'rb') as file_handler:
                self._faces = pickle.load(file_handler)

        else:
            with open(self._file_name, 'wb') as file_handler:
                pickle.dump(self._faces, file_handler)

    @property
    def faces(self):
        return copy(self._faces)

    @property
    def unnamed_faces(self):
        return [face for face in self._faces if face.name == '']

    def add_face(self, face):
        self._faces.append(face)
        with open(self._file_name, 'wb') as file_handler:
            pickle.dump(self._faces, file_handler)

    def __len__(self):
        return len(self._faces)

    def __getitem__(self, item):
        return self._faces[item]
