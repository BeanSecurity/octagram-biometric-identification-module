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
import pythoncom


class AccessControlSystem(IAccessControlSystem):

    def __init__(self):
        FlexServ = win32com.client.Dispatch("FlexServer.FlexServerGlobal")
        self._token = FlexServ.AuthenticateUser("admin", "admin", False)
        _FlexACS = FlexServ.GetObject(token, "FlexACSModule.FlexACS")
        _FlexDB = FlexServ.GetObject(token, "FlexDB.FlexDBModule")
        self._path = "D:\\Октаграм\\client_temp\\" #TODO: брать из конфига
        self._FlexServ_id = pythoncom.CoMarshalInterThreadInterfaceInStream(pythoncom.IID_IDispatch, FlexServ)
        logger = logging.getLogger(__name__)
        logger.debug("FlexACS: {}".format(str(_FlexACS)))
        logger.debug("FlexDB: {}".format(str(_FlexDB)))


    def _get_ACS_and_DB(self):
        if self._FlexServ is None:
            pythoncom.CoInitialize()
            self._FlexServ  = win32com.client.Dispatch(pythoncom.CoGetInterfaceAndReleaseStream(self._FlexServ_id, pythoncom.IID_IDispatch))
            self._FlexACS = FlexServ.GetObject(self._token, "FlexACSModule.FlexACS")
            self._FlexDB = FlexServ.GetObject(self._token, "FlexDB.FlexDBModule")
        return self._FlexACS, self._FlexDB

    #TODO: проверка статуса двери
    def open_door(self, door: ControlPoint, user: User):
        FlexACS, FlexDB = self._get_ACS_and_DB()
        try:
            FlexACS.FlexCommand(
                None, "S-1-0581B9AD-5CDC-4d86-A328-0D94A615A418", 10135)
            # FlexDB.PutEvent(0, user.key_id,
            #                 "S-1-0581B9AD-5CDC-4d86-A328-0D94A615A418", 344, 0,
            #                 datetime.datetime.now(), '', None)
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception(e)

        # TODO: брать SID двери из ControlPoint

    def has_access(self, door: ControlPoint, user: User) -> bool: # можно кэшировать
        FlexACS, FlexDB = self._get_ACS_and_DB()
        try:
            users = FlexDB.GetUsers4Device("S-1-0581B9AD-5CDC-4d86-A328-0D94A615A418")
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
        FlexACS, FlexDB = self._get_ACS_and_DB()
        try:
            users = [User(user.strSID,
                          user.strFirstName+' '+user.strLastName,
                          Vector(''))
                     for user in FlexDB.GetUsers("", False, "")]

        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception(e)
            return None

        return users

