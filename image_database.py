import json
import os
import cv2


class ImageDatabase(object):
    def __init__(self, file_name, folder_name):
        self._counter = 0
        self._file_name = file_name
        self._folder_name = folder_name
        self._folder_path = os.path.join('static', folder_name)

        if os.path.exists(self._file_name):
            with open(self._file_name, 'rb') as file_handler:
                self._counter = json.load(file_handler)

        else:
            self._write_data()

        if not os.path.isdir(self._folder_path):
            os.mkdir(self._folder_path)

    def _write_data(self):
        with open(self._file_name, 'wb') as file_handler:
            json.dump(self._counter, file_handler)

    def save_image(self, image):
        """

        :param image: the image to save
        :return: the saved image's path
        """
        image_name = "{}.jpg".format(self._counter)
        image_path = os.path.join(self._folder_path, image_name)
        cv2.imwrite(image_path, image)

        self._counter += 1
        self._write_data()
        return os.path.join(self._folder_name, image_name)
