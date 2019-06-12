from picamera.array import PiRGBArray
from picamera import PiCamera


class Camera(object):
    def __init__(self, frame_rate, rotation, resolution):
        self._frame_rate = frame_rate
        self._rotation = rotation
        self._resolution = resolution

        self._camera = None
        self._output = None
        self._frame = 0

    def capture(self):
        for frame in self._camera.capture_continuous(self._output, format='bgr'):
            self._frame = frame.array
            yield self._frame
            self._output.truncate()
            self._output.seek(0)

    @property
    def frame(self):
        return self._frame

    def __enter__(self):
        self._camera = PiCamera()
        self._camera.resolution = self._resolution
        self._camera.rotation = self._rotation
        self._camera.framerate = self._frame_rate

        self._output = PiRGBArray(self._camera)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._camera.close()
        self._output.close()
