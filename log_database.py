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
            self._write_data()

    def log_entrance(self, face_id, image_path):
        self._logs.append(Log(face_id, image_path))
        self._write_data()
        return len(self._logs) - 1  # the id of the log

    def update_is_seen(self, log_id):
        self._logs[log_id].is_seen = True
        self._write_data()

    def _write_data(self):
        with open(self._file_name, 'wb') as file_handler:
            pickle.dump(self._logs, file_handler)

    @property
    def logs(self):
        return self._logs

    @property
    def unseen_faces(self):
        return {index: self._logs[index] for index in range(len(self._logs)) if not self._logs[index].is_seen}

    def __getitem__(self, item):
        return self._logs[item]
