from picamera.array import PiRGBArray
from picamera import PiCamera


class Camera(object):
    def __init__(self, **kwargs):
        self._camera_attributes = kwargs
        self._camera = None
        self._output = None

    def capture(self):
        for frame in self._camera.capture_continuous(self._output, format='bgr'):
            yield frame.array
            self._output.truncate()
            self._output.seek(0)

    def __enter__(self):
        self._camera = PiCamera(**self._camera_attributes)
        self._camera.resolution = (640, 480)
        self._camera.framerate = 32

        self._output = PiRGBArray(self._camera)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._camera.close()
        self._output.close()
