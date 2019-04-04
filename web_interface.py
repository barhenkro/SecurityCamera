from flask import Flask, Response, render_template, request, url_for
import cv2
from threading import Thread
from databases import *

_app = Flask('securitycamera')
camera_frame = 0


def run():
    Thread(target=_app.run, kwargs={'host': '0.0.0.0', 'port': 80, 'debug': False, 'threaded': True}).start()


@_app.route('/stream')
def stream():
    def get_page():
        while True:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + get_img_bytes(camera_frame) + b'\r\n')

    return Response(get_page(), mimetype='multipart/x-mixed-replace; boundary=frame')


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


@_app.route('/logs')
def list_logs():
    initial_string = url_for('list_logs') + '/'
    items = create_list_items(log_database.logs, lambda log: log.time_string, initial_string)
    return render_template('list_page.html', title="Logs", list_items=items)


def create_list_items(objects_list, naming_function, initial_string):
    for index in range(len(objects_list)):
        yield (naming_function(objects_list[index]), initial_string + str(index))
