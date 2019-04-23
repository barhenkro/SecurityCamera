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
        face_capture = crop_face(frame, face_location)
        face_encoding = face_recognition.face_encodings(frame, known_face_locations=[face_location])[0]

        # unknown face
        if len(face_database) == 0:
            register_new_face(face_encoding, image_database.save_image(face_capture))

        else:
            for face_id in range(len(face_database)):

                registered_face = face_database[face_id]
                # known face
                if registered_face.compare_face(face_encoding):
                    recognized_face = True

                    if registered_face.time_since_last_seen >= 5:
                        log_database.log_entrance(face_id, image_database.save_image(face_capture))

                    if registered_face.time_since_last_seen >= 1:
                        face_database.update_last_seen(face_id)

            # unknown face
            if not recognized_face:
                register_new_face(face_encoding, image_database.save_image(face_capture))

    return frame


def register_new_face(face_encoding, capture_path):
    face_id = len(face_database)
    face_database.add_face(face_encoding, capture_path)
    log_database.log_entrance(face_id, capture_path)


def crop_face(frame, face_location):
    top, right, bottom, left = face_location
    return frame[top:bottom+1, left:right+1]
