from win32com import client

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
        self._path = "C:\\Program Files (x86)\\Octagram\\client_temp\\" #TODO: брать из конфига

    #TODO: проверка статуса двери
    def open_door(self, door: ControlPoint, user: User): #TODO: добавить отправку события о том, что сотрудник зашел
        self._FlexACS.FlexCommand(None, "S-1-0581B9AD-5CDC-4d86-A328-0D94A615A418", 10135) # TODO: брать SID двери из ControlPoint

    def has_access(self, door: ControlPoint, user: User) -> bool: # можно кэшировать
        users = self._FlexDB.GetUsers4Device("S-1-0581B9AD-5CDC-4d86-A328-0D94A615A418") # TODO: брать SID двери из ControlPoint
        return user.key_id in [u.strSID for u in users]

    def get_user_photo(self, user: User):
        photos = list(filter(lambda f: isfile(join(self._path, f)) and
                                       f.endswith(('.jpeg', '.jpg', '.png', '.JPG')) and
                                       f.startswith(user.key_id),
                             listdir(self._path)))
        if len(photos)==0:
            return None #TODO: исключения

        return self._path + photos[0]

    def get_unidentified_users(self) -> List[User]:
        return [User(user.strSID,
                     user.strFirstName+' '+user.strLastName,
                     Vector(''))
                for user in self._FlexDB.GetUsers("", False, "")]


# import string
# from models.control_point import ControlPoint
# from models.user import User
# from models.vector import Vector
# from services.service_interfaces import IAccessControlSystem
# import random
# from typing import Dict, Tuple, List
#
#
# class AccessControlSystem(IAccessControlSystem):
#
#     def __int__(self):
#         pass
#
#     def open_door(self, door: ControlPoint, user: User):
#         print("OPENED for: " + str(user))
#
#     def has_access(self, door: ControlPoint, user: User) -> bool:
#         return False
#
#     def get_user_photo(self, user: User):  # TODO: забирать изображения из папки
#         pass
#
#     def get_unidentified_users(self) -> List[User]:
#         return [User(''.join(random.choice(string.ascii_lowercase) for i in range(10)),
#                      Vector(''))]