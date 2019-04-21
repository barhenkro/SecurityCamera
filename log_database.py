import os
import pickle
from log import Log


class LogDatabase(object):
    def __init__(self, file_name):
        self._logs = []
        self._file_name = file_name

        if os.path.exists(self._file_name):
            with open(self._file_name, 'rb') as file_handler:
                self._logs = pickle.load(file_handler)

        else:
            with open(self._file_name, 'wb') as file_handler:
                pickle.dump(self._logs, file_handler)

    def log_entrance(self, face_id, image_path):
        self._logs.append(Log(face_id, image_path))

        with open(self._file_name, 'wb') as file_handler:
            pickle.dump(self._logs, file_handler)

    @property
    def logs(self):
        return self._logs
