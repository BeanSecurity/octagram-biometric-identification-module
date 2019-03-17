import win32com.client
import logging
from models.control_point import ControlPoint
from models.user import User
from models.vector import Vector
from services.service_interfaces import IAccessControlSystem
from typing import Dict, Tuple, List
from os import listdir
from os.path import isfile, join


class AccessControlSystem(IAccessControlSystem):

    def __init__(self):
        FlexServ = win32com.client.Dispatch("FlexServer.FlexServerGlobal")
        token = FlexServ.AuthenticateUser("admin", "admin", False)
        self._FlexACS = FlexServ.GetObject(token, "FlexACSModule.FlexACS")
        self._FlexDB = FlexServ.GetObject(token, "FlexDB.FlexDBModule")
        self._path = "D:\\Октаграм\\client_temp\\" #TODO: брать из конфига
        logger = logging.getLogger(__name__)
        logger.debud("FlexACS: {}".format(str(self._FlexACS)))
        logger.debud("FlexDB: {}".format(str(self._FlexDB)))

    #TODO: проверка статуса двери
    def open_door(self, door: ControlPoint, user: User):
        #TODO: добавить отправку события о том, что сотрудник зашел
        try:
            self._FlexACS.FlexCommand(
                None, "S-1-0581B9AD-5CDC-4d86-A328-0D94A615A418", 10135)
            self._FlexDB.PutEvent(0, user.key_id,
                            "S-1-0581B9AD-5CDC-4d86-A328-0D94A615A418", 344, 0,
                            datetime.datetime.now(), '', None)
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception(e)

        # TODO: брать SID двери из ControlPoint

    def has_access(self, door: ControlPoint, user: User) -> bool: # можно кэшировать
        try:
            users = self._FlexDB.GetUsers4Device("S-1-0581B9AD-5CDC-4d86-A328-0D94A615A418")
            # TODO: брать SID двери из ControlPoint
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
            return None #TODO: исключения

        with open(self._path + photos[0], 'rb') as pic:
            return pic

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

