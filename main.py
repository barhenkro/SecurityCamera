import cv2
import face_detection
import web_interface


def main():
    frame = cv2.imread("obama.jpg")
    web_interface.run()

    while True:
        web_interface.camera_frame = face_detection.detect_faces(frame)


if __name__ == '__main__':
    main()
