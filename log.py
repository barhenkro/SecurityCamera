import time


class Log(object):
    def __init__(self, face_id, face_capture):
        self.__time = time.localtime()
        self.__face_id = face_id
        self._face_capture = face_capture

    @property
    def time(self):
        return self.__time

    @property
    def time_string(self):
        return time.asctime(self.__time)