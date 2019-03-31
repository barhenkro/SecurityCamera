import face_recognition


class Face(object):
    def __init__(self, face_encoding, id):
        self._id = id
        self._name = None
        self._face_encodings = [face_encoding]

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def compare_face(self, unknown_face_encoding):
        return True in face_recognition.compare_faces(self._face_encodings, unknown_face_encoding)
