from flask import Flask, Response
import cv2
from threading import Thread


class Streamer(object):
    app = Flask("Streamer")

    def __init__(self):
        self.original_frame = 0
        Streamer.app.add_url_rule("/stream", "stream", self._get_response)

    @staticmethod
    def run():
        Thread(target=lambda: Streamer.app.run(host='0.0.0.0', port=80, debug=False, threaded=True)).start()

    def update(self, original_frame):
        self.original_frame = original_frame

    @staticmethod
    def _get_img_bytes(img):
        _, img = cv2.imencode('.jpg', img)
        return img.tobytes()

    def _get_page(self):
        while True:
            frame = Streamer._get_img_bytes(self.original_frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def _get_response(self):
        return Response(self._get_page(), mimetype='multipart/x-mixed-replace; boundary=frame')
