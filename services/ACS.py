import win32com.client
import logging
from models.control_point import ControlPoint
from models.user import User
from models.vector import Vector
from services.service_interfaces import IAccessControlSystem
from typing import Dict, Tuple, List
from os import listdir
from os.path import isfile, join
import datetime
import time


class AccessControlSystem(IAccessControlSystem):

    def __init__(self):
        FlexServ = win32com.client.Dispatch("FlexServer.FlexServerGlobal")
        token = FlexServ.AuthenticateUser("admin", "admin", False)
        self._FlexACS = FlexServ.GetObject(token, "FlexACSModule.FlexACS")
        self._FlexACS.ConnectAll(None, 0)
        self._FlexDB = FlexServ.GetObject(token, "FlexDB.FlexDBModule")
        self._path = "D:\\Октаграм\\client_temp\\"
        self._last_time_accessed = datetime.datetime.now() - datetime.timedelta(seconds=6)
        self._last_user_accessed = User('','', Vector(''))
        logger = logging.getLogger(__name__)
        logger.debug("FlexACS: {}".format(str(self._FlexACS)))
        logger.debug("FlexDB: {}".format(str(self._FlexDB)))

    def open_door(self, door: ControlPoint, user: User):
        try:
            self._FlexACS.FlexCommand(
                None, "S-1-0581B9AD-5CDC-4d86-A328-0D94A615A418", 10133)
            logger = logging.getLogger(__name__)
            logger.debug(self._last_time_accessed)
            logger.debug(datetime.datetime.now())
            logger.debug(datetime.datetime.now() - self._last_time_accessed)
            logger.debug((datetime.datetime.now() - self._last_time_accessed) > datetime.timedelta(seconds=5))
            logger.debug(self._last_user_accessed.key_id)
            logger.debug(self._last_user_accessed.key_id != user.key_id)
            if ((datetime.datetime.now() - self._last_time_accessed) > datetime.timedelta(seconds=5)) or (self._last_user_accessed.key_id != user.key_id):
                logger.info("Event put for user: " + user.full_name)
                self._FlexDB.PutEvent(0, user.key_id,
                                      "S-1-0581B9AD-5CDC-4d86-A328-0D94A615A418", 289, 0,
                                      datetime.datetime.now()+datetime.timedelta(seconds=-time.timezone), '', None)
                self._last_user_accessed = user
            self._last_time_accessed = datetime.datetime.now()
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception(e)

    def has_access(self, door: ControlPoint, user: User) -> bool:
        try:
            users = self._FlexDB.GetUsers4Device("S-1-0581B9AD-5CDC-4d86-A328-0D94A615A418")
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception(e)
            return False

        if not users:
            return False

        return user.key_id in (u.strSID for u in users)

    def get_user_photo(self, user: User):
        try:
            photos = list(filter(lambda f: isfile(join(self._path, f)) and
                                       f.endswith(('.jpeg', '.jpg', '.png', '.JPG')) and
                                       f.startswith(user.key_id),
                             listdir(self._path)))
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception(e)
            return None

        if len(photos)==0:
            return None

        with open(self._path + photos[0], 'rb') as pic:
            return pic.read()

    def get_unidentified_users(self) -> List[User]:
        try:
            users = [User(user.strSID,
                          user.strFirstName+' '+user.strLastName,
                          Vector(''))
                     for user in self._FlexDB.GetUsers("", False, "")]

        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception(e)
            return None

        return users
