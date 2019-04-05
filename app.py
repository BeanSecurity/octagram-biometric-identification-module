import time
from services.ACS import AccessControlSystem
from services.mocks import MockAccessControlSystem
from services.mocks import MockRecognizer
from services.mocks import MockCameraController
from services.recognizer import *
from services.repository import *
from services.service_interfaces import *
from models.user import User
from models.control_point import *
from core.authorizer import *
from controllers.camera_controllers import *
from controllers.octagram_controllers import *
import logging


if __name__ == '__main__':

    logging.basicConfig(
        handlers=[
            logging.FileHandler("app_logs.log"),
            logging.StreamHandler()
        ],
        level=logging.DEBUG,
        format=
        '%(asctime)s - %(name)s.%(funcName)s - %(levelname)s - %(message)s')

    authorizer = Authorizer(Repository(), Recognizer(),
                            AccessControlSystem())

    camera = CameraController(authorizer, CameraStreamHTTP())
