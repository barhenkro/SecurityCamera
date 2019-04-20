import face_recognition
import time


class Face(object):
    def __init__(self, face_encoding):
        self._name = None
        self._face_encodings = [face_encoding]
        self._last_seen = time.time()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def time_since_last_seen(self):
        return time.time() - self._last_seen

    def update_last_seen(self):
        self._last_seen = time.time()

    def compare_face(self, unknown_face_encoding):
        return True in face_recognition.compare_faces(self._face_encodings, unknown_face_encoding)
