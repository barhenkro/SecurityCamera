from databases import face_database_instance, log_database_instance, image_database_instance
from detection_utils import crop_face
import face_recognition


class FaceDetector(object):

    def __init__(self, notifiers):
        self._notifiers = notifiers

    def detect_faces(self, frame):
        """

        :param frame: a frame to detect faces from
        :return: frame with marked faces
        """
        face_locations = face_recognition.face_locations(frame)

        for face_location in face_locations:
            face_capture = crop_face(frame, face_location)
            face_encoding = face_recognition.face_encodings(frame, known_face_locations=[face_location])[0]

            # unknown face
            if len(face_database_instance) == 0:
                self.register_new_face(face_encoding, image_database_instance.save_image(face_capture))

            else:
                recognized_face = False
                for face_id in range(len(face_database_instance)):

                    registered_face = face_database_instance[face_id]
                    # known face
                    if registered_face.compare_face(face_encoding, 0.5):
                        recognized_face = True

                        if registered_face.time_since_last_seen >= 60:
                            log_id = log_database_instance.log_entrance(face_id, image_database_instance.save_image(
                                face_capture))
                            face_database_instance.register_log(face_id, log_id)
                            self.notify(log_id)

                        if registered_face.time_since_last_seen >= 1:
                            face_database_instance.update_last_seen(face_id)

                # unknown face
                if not recognized_face:
                    self.register_new_face(face_encoding, image_database_instance.save_image(face_capture))

        return frame

    def register_new_face(self, face_encoding, capture_path):
        face_id = len(face_database_instance)
        face_database_instance.add_face(face_encoding, capture_path)
        log_id = log_database_instance.log_entrance(face_id, capture_path)
        face_database_instance.register_log(face_id, log_id)
        self.notify(log_id)

    def notify(self, log_id):
        for notifier in self._notifiers:
            notifier.notify(log_id)
