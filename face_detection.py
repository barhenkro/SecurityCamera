from databases import *
import face_recognition


def detect_faces(frame):
    """

    :param frame: a frame to detect faces from
    :return: frame with marked faces
    """
    recognized_face = False
    face_locations = face_recognition.face_locations(frame)

    for face_location in face_locations:
        face_encoding = face_recognition.face_encodings(frame, known_face_locations=[face_location])[0]

        # unknown face
        if len(face_database) == 0:
            register_new_face(face_encoding, frame)

        else:
            for face_id in range(len(face_database)):

                registered_face = face_database[face_id]
                # known face
                if registered_face.compare_face(face_encoding):
                    recognized_face = True

                    if registered_face.time_since_last_seen >= 5:
                        log_database.log_entrance(face_id, frame)

                    if registered_face.time_since_last_seen >= 1:
                        face_database.update_last_seen(face_id)

            # unknown face
            if not recognized_face:
                register_new_face(face_encoding, frame)

    return frame


def register_new_face(face_encoding, capture):
    face_id = len(face_database)
    face_database.add_face(face_encoding)
    log_database.log_entrance(face_id, capture)
