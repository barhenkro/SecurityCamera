import time


class Log(object):
    def __init__(self, face_id, face_capture):
        self.__time = time.localtime()
        self.__face_id = face_id
        self._face_capture = face_capture
