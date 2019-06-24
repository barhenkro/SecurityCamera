import face_recognition


def crop_face(frame, face_location):
    """

    :param frame:an image to crop the face from
    :param face_location: the location of the face in the image
    :return: an image with only the face in it
    """
    top, right, bottom, left = face_location
    return frame[top:bottom + 1, left:right + 1]


def find_face(image):
    """

    :param image:  an image which contains a face
    :return: (face location, face encoding) only if there is one face, otherwise return None
    """
    face_location = face_encoding = None
    locations = face_recognition.face_locations(image)
    if len(locations) == 1:
        face_location = locations[0]
        face_encoding = face_recognition.face_encodings(image, known_face_locations=[face_location])[0]
    return face_location, face_encoding
