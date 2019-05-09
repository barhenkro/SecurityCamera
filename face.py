import face_recognition
import time


class Face(object):
    def __init__(self, face_encoding, image_path, name):
        self._name = name
        self._face_encodings = [face_encoding]
        self._last_seen = time.time()
        self._image_path = image_path

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def image_path(self):
        return self._image_path

    @image_path.setter
    def image_path(self, path):
        self._image_path = path

    @property
    def time_since_last_seen(self):
        return time.time() - self._last_seen

    def update_last_seen(self):
        self._last_seen = time.time()

    def compare_face(self, unknown_face_encoding):
        return True in face_recognition.compare_faces(self._face_encodings, unknown_face_encoding)
