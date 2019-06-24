from database import Database
import hashlib


class UsersDatabase(Database):
    def __init__(self, filename):
        super(UsersDatabase, self).__init__(filename, initial_data={'admin': hashlib.md5('admin').hexdigest()},
                                            serialization_type='json')

    def check_authentication(self, username, password):
        self._read_data()
        return username in self._data and self._data[username] == hashlib.md5(password).hexdigest()
