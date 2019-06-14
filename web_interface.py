from flask import Flask, Response, render_template, request, url_for, session, redirect, flash
import cv2
from threading import Thread
from databases import face_database_instance, log_database_instance, image_database_instance, users_database_instance
from databases.image_database import ImageDatabase
from flask_utils import create_list_items, login_required
import detection_utils
import os

_app = Flask('securitycamera')
camera_frame = 0


def run():
    _app.secret_key = os.urandom(16)
    Thread(target=_app.run, kwargs={'host': '0.0.0.0', 'port': 80, 'debug': False, 'threaded': True}).start()


@_app.route('/')
@login_required
def home():
    return render_template("index.html", new_faces_counter=len(face_database_instance.unnamed_faces),
                           new_logs_counter=len(log_database_instance.unseen_faces))


@_app.route('/login', methods=['POST', 'GET'])
def login():
    message = "you are not logged in"
    if 'logged' not in session:
        session['logged'] = False

    if request.method == 'POST':
        # password correct
        if users_database_instance.check_authentication(request.form["username"], request.form["password"]):
            session["logged"] = True
            next_site = request.args.get('next')
            # entered directly to login
            if next_site is None:
                next_site = url_for('home')

            return redirect(next_site)
        # incorrect password
        message = "incorrect username or password"

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
    if face_id >= len(face_database_instance):
        return render_template('error.html', not_found="Face"), 404

    if request.method == 'POST':
        face_database_instance.change_name(face_id, request.form['name'])
    return render_template('face.html', face=face_database_instance[face_id], face_id=face_id)


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
            flash("you didn't chose a file")
            return redirect(request.url)

        # every thing is right
        if uploaded_file and ImageDatabase.is_allowed(uploaded_file.filename):

            uploaded_file = ImageDatabase.convert_to_numpy_image(uploaded_file)
            face_location, face_encoding = detection_utils.find_face(uploaded_file)

            # if there is one face in the picture
            if face_location:
                if not face_database_instance.compare_all_faces(face_encoding):
                    image_path = image_database_instance.save_image(
                        detection_utils.crop_face(uploaded_file, face_location))
                    face_database_instance.add_face(face_encoding, image_path, name=request.form['face_name'])
                    flash("face was uploaded successfully")

                else:
                    flash("face already exists in the system")
            else:
                flash("picture should contain exactly one face")

        else:
            flash("file should be a picture")

            # image_path = image_database.save_image(uploaded_file)
            # full_image_path = os.path.join(ImageDatabase.ROOT_FOLDER_NAME, image_path)
            # face_database.add_face(encode_face(full_image_path), image_path, name=request.form['face_name'])
            return redirect(request.url)

    return render_template('new_face.html')


@_app.route('/faces')
@login_required
def list_faces():
    items = [(face.name, url_for('show_face', face_id=index)) for index, face in
             face_database_instance.numbered_faces.iteritems()]
    return render_template('list_page.html', title="Faces", list_items=items)


@_app.route('/unnamed-faces')
@login_required
def list_unnamed_faces():
    initial_string = url_for('list_faces') + '/'
    unnamed_faces_dict = face_database_instance.unnamed_faces
    items = [(face_id, initial_string + str(face_id)) for face_id in unnamed_faces_dict]
    return render_template('list_page.html', title="Unnamed Faces", list_items=items)


@_app.route('/logs/<int:log_id>')
@login_required
def show_log(log_id):
    if log_id >= len(log_database_instance):
        return render_template('error.html', not_found="Log"), 404

    if not log_database_instance[log_id].is_seen:
        log_database_instance.update_is_seen(log_id)

    face_name = face_database_instance[log_database_instance[log_id].face_id].name
    return render_template('log.html', log=log_database_instance[log_id], face_name=face_name)


@_app.route('/logs')
@login_required
def list_logs():
    initial_string = url_for('list_logs') + '/'
    items = create_list_items(log_database_instance.logs, lambda log: log.time_string, initial_string)
    return render_template('list_page.html', title="Logs", list_items=items)


@_app.route('/unnamed-logs')
@login_required
def list_unnamed_logs():
    initial_string = url_for('list_logs') + '/'
    unseen_logs_dict = log_database_instance.unseen_faces
    items = [(unseen_logs_dict[log_id].time_string, initial_string + str(log_id)) for log_id in unseen_logs_dict]
    return render_template('list_page.html', title="Unseen Logs", list_items=items)


@_app.route('/face-logs/<int:face_id>')
def list_logs_by_face_id(face_id):
    if face_id >= len(face_database_instance):
        return render_template('error.html', not_found="Face"), 404

    face = face_database_instance[face_id]
    logs_id = face.logs_id
    logs = log_database_instance[logs_id]
    titles = [log.time_string for log in logs]
    links = [url_for('show_log', log_id=log_id) for log_id in logs_id]

    items = zip(titles, links)
    return render_template('list_page.html', title="Face's Logs", list_items=items)


@_app.errorhandler(404)
def not_found(eror):
    return render_template('error.html', not_found="Page"), 404


@_app.route('/merge-faces', methods=['GET', 'POST'])
@login_required
def merge_faces():
    if request.method == "POST":
        # get ids
        merge_from_id = int(request.form["merge-from-face"])
        merge_to_id = int(request.form["merge-to-face"])

        # merge manipulations
        merge_from_logs_id = face_database_instance[merge_from_id].logs_id
        face_database_instance.merge_faces(merge_from_id, merge_to_id)
        log_database_instance.change_face_id(merge_from_logs_id, merge_to_id)
        del face_database_instance[merge_from_id]

    numbered_faces = face_database_instance.numbered_faces
    return render_template('merge_faces.html', faces=numbered_faces)
