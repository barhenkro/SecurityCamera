from face_database import FaceDatabase
from face import Face
from log_database import LogDatabase
import cv2
import face_recognition


def main():
    # video_capture = cv2.VideoCapture(0)
    face_database = FaceDatabase("faces.txt")
    log_database = LogDatabase('logs.txt')
    frame = cv2.imread("obama2.jpg")

    while True:
        # _, frame = video_capture.read()
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, known_face_locations=face_locations)
        for face_encoding in face_encodings:

            # unknown face
            if len(face_database.faces) == 0:
                new_face = Face(face_encoding, len(face_database.faces))
                face_database.add_face(new_face)
                log_database.log_entrance(new_face.id, frame)

            else:
                for face in face_database.faces:
                    # known face
                    if face.compare_face(face_encoding):
                        log_database.log_entrance(face.id, frame)

                    # unknown face
                    else:
                        new_face = Face(face_encoding, len(face_database.faces))
                        face_database.add_face(new_face)
                        log_database.log_entrance(new_face.id, frame)


if __name__ == '__main__':
    main()
