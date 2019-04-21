import time


class Log(object):
    def __init__(self, face_id, image_path):
        self._time = time.localtime()
        self._face_id = face_id
        self._image_path = image_path

    @property
    def time(self):
        return self._time

    @property
    def time_string(self):
        return time.asctime(self._time)
