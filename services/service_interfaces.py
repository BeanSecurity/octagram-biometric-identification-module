import abc
from models.vector import Vector
from models.control_point import ControlPoint
from models.user import User
from typing import Dict, Tuple, List


class IRecognizer(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def extract(self, picture) -> Vector:
        pass

    @abc.abstractmethod
    def compare_vectors(self, user_vector: Vector, extracted_vector: Vector) -> float:
        pass


class IAccessControlSystem(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def open_door(self, door: ControlPoint, user: User):
        pass

    @abc.abstractmethod
    def has_access(self, door: ControlPoint, user: User) -> bool:
        pass


class IRepository(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_users(self) -> List[User]:
        pass

    @abc.abstractmethod
    def get_control_points(self) -> List[ControlPoint]:
        pass

    @abc.abstractmethod
    def get_cameras(self):  # TODO: разобраться с сущностями камер
        pass


class IAuthorizer(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def authorize(self, image):
        pass