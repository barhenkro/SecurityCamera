from face import Face
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
            self._write_data()

    @property
    def faces(self):
        return copy(self._faces)

    @property
    def unnamed_faces(self):
        return {index: self._faces[index] for index in range(self.__len__()) if self._faces[index].name is None}

    def add_face(self, face_encoding, face_image_path, **kwargs):
        name = None
        if 'name' in kwargs:
            name = kwargs['name']

        self._faces.append(Face(face_encoding, face_image_path, name))
        self._write_data()

    def change_name(self, face_id, name):
        self._faces[face_id].name = name
        self._write_data()

    def update_last_seen(self, face_id):
        self._faces[face_id].update_last_seen()
        self._write_data()

    def _write_data(self):
        with open(self._file_name, 'wb') as file_handler:
            pickle.dump(self._faces, file_handler)

    def compare_all_faces(self, face_encoding):
        for face in self._faces:
            if face.compare_face(face_encoding):
                return True
        return False

    def __len__(self):
        return len(self._faces)

    def __getitem__(self, item):
        return self._faces[item]
