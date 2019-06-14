import face_recognition
import time


class Face(object):
    def __init__(self, face_encoding, image_path, name):
        self._name = name
        self._face_encodings = [face_encoding]
        self._last_seen = time.time()
        self._image_path = image_path
        self._logs_id = []

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

    @property
    def logs_id(self):
        return self._logs_id

    def register_log(self, log_id):
        self._logs_id.append(log_id)

    def update_last_seen(self):
        self._last_seen = time.time()

    def compare_face(self, unknown_face_encoding, tolerance):
        return True in face_recognition.compare_faces(self._face_encodings, unknown_face_encoding, tolerance)

    def merge(self, another_face):
        # combine encodings
        self._face_encodings += another_face._face_encodings

        # combine logs
        self._logs_id += another_face.logs_id

        # update last seen
        if self._last_seen < another_face._last_seen:
            self._last_seen = another_face._last_seen
