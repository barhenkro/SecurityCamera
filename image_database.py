import json
import os
import cv2


class ImageDatabase(object):
    def __init__(self, file_name, folder_name):
        self._counter = 0
        self._file_name = file_name
        self._folder_name = folder_name

        if os.path.exists(self._file_name):
            with open(self._file_name, 'rb') as file_handler:
                self._counter = json.load(file_handler)

        else:
            self._write_data()

        if not os.path.isdir(self._folder_name):
            os.mkdir(self._folder_name)

    def _write_data(self):
        with open(self._file_name, 'wb') as file_handler:
            json.dump(self._counter, file_handler)

    def save_image(self, image):
        """

        :param image: the image to save
        :return: the saved image's path
        """
        image_path = "{folder}/{name}.jpg".format(folder=self._folder_name, name=self._counter)
        cv2.imwrite(image_path, image)

        self._counter += 1
        self._write_data()
        return image_path


i = ImageDatabase('images counter.txt', 'images')
i.save_image(cv2.imread('obama.jpg'))
