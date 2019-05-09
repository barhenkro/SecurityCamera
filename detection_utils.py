import face_recognition


def crop_face(frame, face_location):
    """

    :param frame:an image to crop the face from
    :param face_location: the location of the face in the image
    :return: an image with only the face in it
    """
    top, right, bottom, left = face_location
    return frame[top:bottom + 1, left:right + 1]


def encode_face(image_path):
    """

    :param image_path: path to an image which contains a face
    :return: face encoding
    """
    image = face_recognition.load_image_file(image_path)
    return face_recognition.face_encodings(image)[0]
