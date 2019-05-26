from database import Database
from log import Log


class LogDatabase(Database):
    def __init__(self, file_name):
        super(LogDatabase, self).__init__(file_name)

    def log_entrance(self, face_id, image_path):
        self._data.append(Log(face_id, image_path))
        self._write_data()
        return len(self._data) - 1  # the id of the log

    def update_is_seen(self, log_id):
        self._data[log_id].is_seen = True
        self._write_data()

    @property
    def logs(self):
        self._read_data()
        return self._data

    @property
    def unseen_faces(self):
        self._read_data()
        return {index: self._data[index] for index in range(len(self._data)) if not self._data[index].is_seen}

    def __getitem__(self, item):
        self._read_data()
        return self._data[item]
