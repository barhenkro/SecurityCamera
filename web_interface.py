from flask import Flask, Response
import cv2
from threading import Thread

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
