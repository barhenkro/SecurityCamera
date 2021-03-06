from face import Face
from copy import copy
from database import Database


class FaceDatabase(Database):
    def __init__(self, file_name):
        super(FaceDatabase, self).__init__(file_name)

    @property
    def faces(self):
        self._read_data()
        return copy([face for face in self._data if face is not None])

    @property
    def numbered_faces(self):
        return {index: self._data[index] for index in range(self.__len__()) if self._data[index] is not None}

    @property
    def unnamed_faces(self):
        self._read_data()
        return {index: self._data[index] for index in range(self.__len__()) if
                self._data[index] is not None and self._data[index].name is None}

    def add_face(self, face_encoding, face_image_path, **kwargs):
        name = None
        if 'name' in kwargs:
            name = kwargs['name']

        self._read_data()
        self._data.append(Face(face_encoding, face_image_path, name))
        self._write_data()

    def change_name(self, face_id, name):
        self._read_data()
        self._data[face_id].name = name
        self._write_data()

    def update_last_seen(self, face_id):
        self._read_data()
        self._data[face_id].update_last_seen()
        self._write_data()

    def compare_all_faces(self, face_encoding):
        self._read_data()
        for face in self._data:
            if face is not None and face.compare_face(face_encoding, 0.5):
                return True
        return False

    def register_log(self, face_id, log_id):
        self._read_data()
        self._data[face_id].register_log(log_id)
        self._write_data()

    def merge_faces(self, merge_from_id, merge_to_id):
        """

        :param merge_from_id: the id of the face that being merged
        :param merge_to_id: the id of the face that dose the meging
        :return:
        """
        self._read_data()
        self._data[merge_to_id].merge(self._data[merge_from_id])
        self._write_data()
