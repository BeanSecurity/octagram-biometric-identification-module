import requests
import threading
import time
from services.service_interfaces import IAuthorizer


class CameraController():

    def __init__(self, authorizer: IAuthorizer):
        self.__is_shut_down = threading.Event()
        self.__shutdown_request = False
        self._authorizer = authorizer

    def monitor_camera_forever(self, minimal_request_interval=0.3):
        url = 'http://admin:admin1admin@192.168.1.64/Streaming/channels/1/picture?snapShotImageType=JPEG'
        # url = "https://steamuserimages-a.akamaihd.net/ugc/871874299382774828/952AECC7D2090BED0547A6A60E7AEA65E24D6178/"
        try:
            while not self.__shutdown_request:
                time_before_request = time.monotonic()
                response = requests.get(url, stream=True)
                img = response.raw
                self._authorizer.authorize(img)
                elapsed_time = time.monotonic() - time_before_request
                if elapsed_time < minimal_request_interval:
                    time.sleep(minimal_request_interval - elapsed_time)
        finally:
            self.__shutdown_request = False
            self.__is_shut_down.set()

    def shutdown(self):
        self.__shutdown_request = True
        self.__is_shut_down.wait()