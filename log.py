import time


class Log(object):
    def __init__(self, face_id, image_path):
        self._time = time.localtime()
        self._face_id = face_id
        self._image_path = image_path
        self._is_seen = False

    @property
    def time(self):
        return self._time

    @property
    def time_string(self):
        return time.asctime(self._time)

    @property
    def image_path(self):
        return self._image_path

    @property
    def face_id(self):
        return self._face_id

    @property
    def is_seen(self):
        return self._is_seen

    @is_seen.setter
    def is_seen(self, value):
        self._is_seen = value
