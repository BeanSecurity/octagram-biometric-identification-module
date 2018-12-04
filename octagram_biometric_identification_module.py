import time
from flask import Flask
from services.ACS import *
from services.recognizer import *
from services.repository import *
from services.service_interfaces import *
from models.user import User
from models.control_point import *
from core.authorizer import *
from controllers.camera_controllers import *
from controllers.octagram_controllers import *

app = Flask(__name__)

#
# @app.route('/')
# def hello_world():
#     return 'Hello World!'


if __name__ == '__main__': #TODO: добавить логгирование
    authorizer = Authorizer(Repository(), Recognizer(), AccessControlSystem())

    camera = CameraController(authorizer)
    t = threading.Thread(target=camera.monitor_camera_forever, args=())
    t.setDaemon(True)
    t.start()

    app.run()