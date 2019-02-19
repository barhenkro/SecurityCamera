import time


class Log(object):
    def __init__(self,face_capture):
        self.__time = time.localtime()
        self.__face_id = -1
        self._face_capture = face_capture
