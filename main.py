import cv2
from face_detector_factory import create_face_detector
import web_interface
import json


def main():
    frame = cv2.imread("obama.jpg")
    web_interface.run()

    with open('settings.json', 'rb') as file_handler:
        settings = json.load(file_handler)

    face_detector = create_face_detector(settings)

    while True:
        web_interface.camera_frame = face_detector.detect_faces(frame)


if __name__ == '__main__':
    main()
