from multiprocessing import Process
import json
from face_detector_factory import create_face_detector
from numpy import ndarray


class DetectionProcess(Process):
    def __init__(self, connection):
        super(DetectionProcess, self).__init__()
        self.__connection = connection

        with open('settings.json', 'rb') as file_handler:
            settings = json.load(file_handler)

        self.__face_detector = create_face_detector(settings)

    def run(self):
        while True:
            self.__connection.send('ready')
            frame = self.__connection.recv()

            if type(frame) is ndarray:
                self.__face_detector.detect_faces(frame)
