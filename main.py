import web_interface
from camera import Camera
from detection_process import DetectionProcess
from multiprocessing import Pipe
from threading import Thread


def main():
    child_connection, parent_connection = Pipe()
    detection_process = DetectionProcess(child_connection)
    detection_process.start()

    with Camera() as camera:
        Thread(target=detect_frame, args=(camera, parent_connection)).start()

        for frame in camera.capture():
            web_interface.camera_frame = camera.frame


def detect_frame(camera, connection):
    while True:
        connection.recv()
        connection.send(camera.frame)


if __name__ == '__main__':
    main()
