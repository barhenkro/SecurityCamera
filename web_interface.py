from flask import Flask, Response, render_template, request, url_for, session, redirect
import cv2
from threading import Thread
from databases import *
from flask_utils import create_list_items, login_required
from detection_utils import encode_face
from face_detector import FaceDetector
import os

_app = Flask('securitycamera')
_face_detector = FaceDetector(register_logs=False)
camera_frame = 0


def run():
    _app.secret_key = os.urandom(16)
    Thread(target=_app.run, kwargs={'host': '0.0.0.0', 'port': 80, 'debug': False, 'threaded': True}).start()


@_app.route('/')
@login_required
def home():
    return render_template("index.html", new_faces_counter=len(face_database.unnamed_faces),
                           new_logs_counter=len(log_database.unseen_faces))


@_app.route('/login', methods=['POST', 'GET'])
def login():
    message = "you are not logged in"
    if request.method == 'POST':
        # password correct
        if request.form["password"] == "1234":
            session["logged"] = True
            return redirect(request.args.get('next'))
        # incorrect password
        message = "incorrect password"

    if session["logged"]:
        return redirect(url_for('home'))
    return render_template("login.html", message=message)


@_app.route('/stream_feed')
@login_required
def stream_feed():
    def get_page():
        while True:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + get_img_bytes(camera_frame) + b'\r\n')

    return Response(get_page(), mimetype='multipart/x-mixed-replace; boundary=frame')


@_app.route('/stream')
@login_required
def stream_page():
    return render_template('stream.html')


def get_img_bytes(img):
    _, img = cv2.imencode('.jpg', img)
    return img.tobytes()


@_app.route('/faces/<int:face_id>', methods=['POST', 'GET'])
@login_required
def show_face(face_id):
    if request.method == 'POST':
        face_database.change_name(face_id, request.form['name'])
    return render_template('face.html', face=face_database[face_id])


@_app.route('/add_face', methods=['GET', 'POST'])
@login_required
def add_face():
    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)

        uploaded_file = request.files['file']

        # empty file name
        if uploaded_file.filename == '':
            return redirect(request.url)

        # every thing is right
        if uploaded_file and ImageDatabase.is_allowed(uploaded_file.filename):
            uploaded_file = ImageDatabase.convert_to_numpy_image(uploaded_file)
            """
            image_path = image_database.save_image(uploaded_file)
            full_image_path = os.path.join(ImageDatabase.ROOT_FOLDER_NAME, image_path)
            face_database.add_face(encode_face(full_image_path), image_path, name=request.form['face_name'])
            """
            _face_detector.detect_faces(uploaded_file)
            return redirect(request.url)

    return render_template('new_face.html')


@_app.route('/faces')
@login_required
def list_faces():
    initial_string = url_for('list_faces') + '/'
    items = create_list_items(face_database.faces, lambda face: face.name, initial_string)
    return render_template('list_page.html', title="Faces", list_items=items)


@_app.route('/unnamed-faces')
@login_required
def list_unnamed_faces():
    initial_string = url_for('list_faces') + '/'
    unnamed_faces_dict = face_database.unnamed_faces
    items = [(face_id, initial_string + str(face_id)) for face_id in unnamed_faces_dict]
    return render_template('list_page.html', title="Unnamed Faces", list_items=items)


@_app.route('/logs/<int:log_id>')
@login_required
def show_log(log_id):
    if not log_database[log_id].is_seen:
        log_database.update_is_seen(log_id)

    face_name = face_database[log_database[log_id].face_id].name
    return render_template('log.html', log=log_database[log_id], face_name=face_name)


@_app.route('/logs')
@login_required
def list_logs():
    initial_string = url_for('list_logs') + '/'
    items = create_list_items(log_database.logs, lambda log: log.time_string, initial_string)
    return render_template('list_page.html', title="Logs", list_items=items)


@_app.route('/unnamed-logs')
@login_required
def list_unnamed_logs():
    initial_string = url_for('list_logs') + '/'
    unseen_logs_dict = log_database.unseen_faces
    items = [(unseen_logs_dict[log_id].time_string, initial_string + str(log_id)) for log_id in unseen_logs_dict]
    return render_template('list_page.html', title="Unseen Logs", list_items=items)
