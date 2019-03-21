import time
# from flask import Flask
try:
    from services.ACS import AccessControlSystem
except Exception as e:
    # logger.exception(e)
    # logger.debug("ACS was mocked")
    from services.mocks import MockAccessControlSystem as AccessControlSystem
from services.mocks import MockRecognizer
from services.recognizer import *
from services.repository import *
from services.service_interfaces import *
from models.user import User
from models.control_point import *
from core.authorizer import *
from controllers.camera_controllers import *
from controllers.octagram_controllers import *
import logging
# from win32com import client

# app = Flask(__name__)

#
# @app.route('/')
# def hello_world():
#     return 'Hello World!'

if __name__ == '__main__':  # TODO: добавить логгирование

    logging.basicConfig(  # filename='application.log'
        handlers=[
            logging.FileHandler("OBIM.log"),
            logging.StreamHandler()
        ],
        level=logging.DEBUG,
        format=
        '%(asctime)s - %(name)s.%(funcName)s - %(levelname)s - %(message)s')

    authorizer = Authorizer(Repository(), MockRecognizer(),
                            AccessControlSystem())

    camera = CameraController(authorizer, CameraStreamVLC())
    # camera._monitor_camera_forever()
    # t = threading.Thread(target=camera.monitor_camera_forever, args=())
    # t.setDaemon(True)
    # t.start()

    # app.run()
