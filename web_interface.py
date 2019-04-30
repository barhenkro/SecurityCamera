from flask import Flask, Response, render_template, request, url_for
import cv2
from threading import Thread
from databases import *

_app = Flask('securitycamera')
camera_frame = 0


def run():
    Thread(target=_app.run, kwargs={'host': '0.0.0.0', 'port': 80, 'debug': False, 'threaded': True}).start()


@_app.route('/')
def home():
    return render_template("index.html", new_faces_counter=len(face_database.unnamed_faces), new_logs_counter=0)


@_app.route('/stream_feed')
def stream_feed():
    def get_page():
        while True:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + get_img_bytes(camera_frame) + b'\r\n')

    return Response(get_page(), mimetype='multipart/x-mixed-replace; boundary=frame')


@_app.route('/stream')
def stream_page():
    return render_template('stream.html')


def get_img_bytes(img):
    _, img = cv2.imencode('.jpg', img)
    return img.tobytes()


@_app.route('/faces/<int:face_id>', methods=['POST', 'GET'])
def show_face(face_id):
    if request.method == 'POST':
        face_database.change_name(face_id, request.form['name'])
    return render_template('face.html', face=face_database[face_id])


@_app.route('/faces')
def list_faces():
    initial_string = url_for('list_faces') + '/'
    items = create_list_items(face_database.faces, lambda face: face.name, initial_string)
    return render_template('list_page.html', title="Faces", list_items=items)


@_app.route('/unnamed-faces')
def list_unnamed_faces():
    initial_string = url_for('list_faces') + '/'
    unnamed_faces_dict = face_database.unnamed_faces
    items = [(face_id, initial_string + str(face_id)) for face_id in unnamed_faces_dict]
    return render_template('list_page.html', title="Unnamed Faces", list_items=items)


@_app.route('/logs/<int:log_id>')
def show_log(log_id):
    face_name = face_database[log_database[log_id].face_id].name
    return render_template('log.html', log=log_database[log_id], face_name=face_name)


@_app.route('/logs')
def list_logs():
    initial_string = url_for('list_logs') + '/'
    items = create_list_items(log_database.logs, lambda log: log.time_string, initial_string)
    return render_template('list_page.html', title="Logs", list_items=items)


def create_list_items(objects_list, naming_function, initial_string):
    for index in range(len(objects_list)):
        yield (naming_function(objects_list[index]), initial_string + str(index))
