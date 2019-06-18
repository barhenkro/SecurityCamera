from database import Database
import os
import cv2
import tempfile
import math


class ImageDatabase(Database):
    ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
    ROOT_FOLDER_NAME = 'static'
    FOLDER_NAME = 'images'
    IMAGE_SIZE = float(100 * 100)
    FOLDER_PATH = os.path.join(ROOT_FOLDER_NAME, FOLDER_NAME)

    def __init__(self, file_name):
        super(ImageDatabase, self).__init__(file_name, initial_data=0, serialization_type='json')

        if not os.path.isdir(ImageDatabase.FOLDER_PATH):
            os.mkdir(ImageDatabase.FOLDER_PATH)

    def save_image(self, image):
        """

        :param image: the image to save
        :return: the saved image's path
        """
        image_name = "{}.jpg".format(self._data)
        image_path = os.path.join(ImageDatabase.FOLDER_PATH, image_name)

        cv2.imwrite(image_path, self.__resize_image(image))

        self._data += 1
        self._write_data()

        return os.path.join(ImageDatabase.FOLDER_NAME, image_name)

    @staticmethod
    def __resize_image(image):
        """

        :param image: the image to resize
        :return: an resized image. enlarged if smaller than desired else shrinked
        """
        current_size = image.shape[0] * image.shape[1]
        factor = math.sqrt(ImageDatabase.IMAGE_SIZE / current_size)
        new_size = (int(image.shape[0] * factor), int(image.shape[1] * factor))
        interpolation = cv2.INTER_CUBIC if current_size < new_size else cv2.INTER_AREA
        return cv2.resize(image, new_size, interpolation=interpolation)

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
