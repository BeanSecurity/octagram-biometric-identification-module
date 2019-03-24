import threading
import time
from services.service_interfaces import IAuthorizer, ICameraStream
import logging
from services.hik_camera import HikCamObject, HikSensor


class CameraController():
    def __init__(self, authorizer: IAuthorizer, camera_stream: ICameraStream):
        self._authorizer = authorizer
        self._camera_stream = camera_stream

        self._thread_active = threading.Event()
        self._thread = threading.Thread(target=self._sensors_polling)
        self._thread.start()

        self._monitor_camera_forever()

        # self.cam = hikvision.HikCamera('http://192.168.1.64', 80, 'admin',
        #                                'admin1admin')
        # self._name = self.cam.get_name
        # self.motion = self.cam.current_motion_detection_state
        # self.cam.start_stream()

        # self._event_states = self.cam.current_event_states
        # self._id = self.cam.get_id

        # print('NAME: {}'.format(self._name))
        # print('ID: {}'.format(self._id))
        # print('{}'.format(self._event_states))
        # print('Motion Dectect State: {}'.format(self.motion))

    def _sensors_polling(self):
        self.camera = HikCamObject('http://192.168.1.64', 80, 'admin', 'admin1admin')
        self.sensors = []
        for sensor, channel_list in self.camera.sensors.items():
            for channel in channel_list:
                self.sensors.append(
                    HikSensor(sensor, channel[1], self.camera, self._callback))

    def _callback(self, message):
        if self.sensors[0].is_on:
            self._thread_active.set()
        else:
            self._thread_active.clear()

    def _monitor_camera_forever(self):
        try:
            while True:
                try:
                    self._thread_active.wait()
                    img = self._camera_stream.get_frame()
                    self._authorizer.authorize(img)
                except Exception as e:
                    logger = logging.getLogger(__name__)
                    logger.exception(e)

        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception(e)

        finally:
            self._thread_active.clear()

class CameraStreamHTTP(ICameraStream):
    def __init__(self):
        import requests
        self._url = 'http://admin:admin1admin@192.168.1.64/Streaming/channels/1/picture?snapShotImageType=JPEG'
        # self._url = "https://24smi.org/public/media/celebrity/2017/02/14/VTbS2hRAEwfe_vladimir-putin.jpg"

    def get_frame(self):
        response = requests.get(self._url, stream=True)
        img = response.content
        return pic


class CameraStreamCV2(ICameraStream):
    def __init__(self):
        import cv2
        import io
        import numpy as np
        import matplotlib.pyplot as plt

        self._video_capture = cv2.VideoCapture(
            "rtsp://admin:admin1admin@192.168.1.64:554/Streaming/channels/1")

    def get_frame(self):
        success, pic = self._video_capture.read()
        if success:
            buf = io.BytesIO()
            pic = cv2.resize(pic, (1280, 720))
            plt.imsave(buf, pic, format='png')
            pic_data = buf.getvalue()
            return pic_data


class CameraStreamVLC(ICameraStream):
    def __init__(self):
        import vlc
        self._player = vlc.MediaPlayer(
            'rtsp://admin:admin1admin@192.168.1.64:554/Streaming/channels/1')
        self._player.play()

    def get_frame(self):
        self._player.video_take_snapshot(0, 'snapshot_camera.tmp.png', 720,
                                         1280)
        with open('snapshot_camera.tmp.png', 'rb') as pic:
            return pic.read()
