from face_database import FaceDatabase
from image_database import ImageDatabase
from log_database import LogDatabase
from users_database import UsersDatabase

face_database_instance = FaceDatabase('faces.txt')
log_database_instance = LogDatabase('logs.txt')
image_database_instance = ImageDatabase('image_counter')
users_database_instance = UsersDatabase('users.json')
