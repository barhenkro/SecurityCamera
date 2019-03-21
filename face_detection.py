from databases import *
from face import Face
import face_recognition


def detect_faces(frame):
    """

    :param frame: a frame to detect faces from
    :return: frame with marked faces
    """
    face_locations = face_recognition.face_locations(frame)

    for face_location in face_locations:
        face_encoding = face_recognition.face_encodings(frame, known_face_locations=[face_location])[0]

        # unknown face
        if len(face_database) == 0:
            register_new_face(face_encoding, frame)

        else:
            for face in face_database.faces:
                # known face
                if face.compare_face(face_encoding):
                    log_database.log_entrance(face.id, frame)
                    break

            # unknown face
            else:
                register_new_face(face_encoding, frame)

    return frame


def register_new_face(face_encoding, capture):
    new_face = Face(face_encoding, len(face_database))
    face_database.add_face(new_face)
    log_database.log_entrance(new_face.id, capture)
