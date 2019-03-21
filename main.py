import cv2
import face_detection


def main():
    frame = cv2.imread("obama.jpg")

    while True:
        frame = face_detection.detect_faces(frame)


if __name__ == '__main__':
    main()
