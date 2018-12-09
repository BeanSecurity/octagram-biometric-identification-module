from models.user import User
from models.control_point import ControlPoint
from models.cam import Camera

from typing import Dict, Tuple, List

from models.vector import Vector
from services.service_interfaces import IRepository


class Repository(IRepository):  # TODO: обращение к базе данных
    def __init__(self):
        self._control_points = [ControlPoint('1', '1')]
        self._cameras = [Camera('1', ControlPoint('1', '1'))]
        self._users = [User('1', Vector('1ab123')), User('2', Vector('2ab123'))]

    def get_users(self) -> List[User]:
        return self._users

    def get_control_points(self) -> List[ControlPoint]:
        return self._control_points

    def get_cameras(self) -> List[Camera]:
        return self._cameras

    def save_user(self, user: User):
        self._users.append(user)