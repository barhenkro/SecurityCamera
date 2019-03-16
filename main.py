from face_database import FaceDatabase
from face import Face
from log_database import LogDatabase
import cv2
import face_recognition
from streamer import Streamer


def main():
    # video_capture = cv2.VideoCapture(0)
    face_database = FaceDatabase("faces.txt")
    log_database = LogDatabase('logs.txt')
    frame = cv2.imread("obama.jpg")
    streamer = Streamer()
    Streamer.run()

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

        # mark the faces
        for face_location in face_locations:
            (top, right, bottom, left) = face_location
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255))
        streamer.update(frame)


if __name__ == '__main__':
    main()
