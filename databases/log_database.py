from database import Database
from log import Log


class LogDatabase(Database):
    def __init__(self, file_name):
        super(LogDatabase, self).__init__(file_name)

    def log_entrance(self, face_id, image_path):
        self._read_data()
        self._data.append(Log(face_id, image_path))
        self._write_data()
        return len(self._data) - 1  # the id of the log

    def update_is_seen(self, log_id):
        self._read_data()
        self._data[log_id].is_seen = True
        self._write_data()

    def change_face_id(self, logs_id_list, new_face_id):
        self._read_data()
        for log_id in logs_id_list:
            self._data[log_id].face_id = new_face_id
        self._write_data()

    @property
    def logs(self):
        self._read_data()
        return {index: self._data[index] for index in range(len(self._data)) if self._data[index] is not None}

    @property
    def unseen_faces(self):
        self._read_data()
        return {index: self._data[index] for index in range(len(self._data)) if
                self._data[index] is not None and not self._data[index].is_seen}
