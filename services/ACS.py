from win32com import client

from models.control_point import ControlPoint
from models.user import User
from services.service_interfaces import IAccessControlSystem


class AccessControlSystem(IAccessControlSystem):

    def __int__(self):
        FlexServ = win32com.client.Dispatch("FlexServer.FlexServerGlobal")
        token = FlexServ.AuthenticateUser("admin", "admin", False)
        self._FlexACS = FlexServ.GetObject(token, "FlexACSModule.FlexACS")
        self._FlexDB = FlexServ.GetObject(token, "FlexDB.FlexDBModule")

    #TODO: проверка статуса двери
    def open_door(self, door: ControlPoint, user: User): #TODO: добавить отправку события о том, что сотрудник зашел
        self._FlexACS.FlexCommand(None, "S-1-0581B9AD-5CDC-4d86-A328-0D94A615A418", 10135) # TODO: брать SID двери из ControlPoint

    def has_access(self, door: ControlPoint, user: User) -> bool: # можно кэшировать
        Users = self._FlexDB.GetUsers4Device("S-1-0581B9AD-5CDC-4d86-A328-0D94A615A418") # TODO: брать SID двери из ControlPoint
        return User.key_id in [u.strSID for u in Users]


#
# from models.control_point import ControlPoint
# from models.user import User
# from services.service_interfaces import IAccessControlSystem
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
#         return True
