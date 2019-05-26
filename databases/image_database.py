from database import Database
import os
import cv2
import tempfile


class ImageDatabase(Database):
    ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
    ROOT_FOLDER_NAME = 'static'
    FOLDER_NAME = 'images'
    FOLDER_PATH = os.path.join(ROOT_FOLDER_NAME, FOLDER_NAME)

    def __init__(self, file_name):
        super(ImageDatabase, self).__init__(file_name, initial_data=0, serialization_type='json')

    def save_image(self, image):
        """

        :param image: the image to save
        :return: the saved image's path
        """
        image_name = "{}.jpg".format(self._data)
        image_path = os.path.join(ImageDatabase.FOLDER_PATH, image_name)

        cv2.imwrite(image_path, image)

        self._data += 1
        self._write_data()

        return os.path.join(ImageDatabase.FOLDER_NAME, image_name)

    @staticmethod
    def is_allowed(file_name):
        return '.' in file_name and file_name.rsplit('.', 1)[1].lower() in ImageDatabase.ALLOWED_EXTENSIONS

    @staticmethod
    def convert_to_numpy_image(image):
        """

        :param image: image from werkzeug.FileStorage
        :return: the image as numpy.ndarray
        """
        with tempfile.NamedTemporaryFile(delete=False) as temp_file_handler:
            temp_file_handler.write(image.read())
            temp_file_path = temp_file_handler.name

        converted_image = cv2.imread(temp_file_path)
        os.unlink(temp_file_path)

        return converted_image
