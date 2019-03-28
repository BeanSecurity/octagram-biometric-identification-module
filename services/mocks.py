import string
from models.control_point import ControlPoint
from models.user import User
from models.vector import Vector
from services.service_interfaces import IAccessControlSystem
import random
from typing import Dict, Tuple, List
from os import listdir
from os.path import isfile, join


class MockAccessControlSystem(IAccessControlSystem):
    def __init__(self):
        pass

    def open_door(self, door: ControlPoint, user: User):
        print("OPENED for: " + str(user))

    def has_access(self, door: ControlPoint, user: User) -> bool:
        return True

    def get_user_photo(self, user: User):
        _path = "D:\\Октаграм\\client_temp\\"
        photos = list(filter(lambda f: isfile(join(_path, f)) and
                             f.endswith(('.jpeg', '.jpg', '.png', '.JPG')),
                             listdir(_path)))
        with open(_path + photos[2], 'rb') as pic:
            picture = pic.read()

    def get_unidentified_users(self) -> List[User]:
        return [
            User(
                ''.join(
                    random.choice(string.ascii_lowercase) for i in range(10)),
                ''.join(
                    random.choice(string.ascii_lowercase) for i in range(10)),
                Vector('')),
            User(
                ''.join(
                    random.choice(string.ascii_lowercase) for i in range(10)),
                ''.join(
                    random.choice(string.ascii_lowercase) for i in range(10)),
                Vector('')),
            User(
                ''.join(
                    random.choice(string.ascii_lowercase) for i in range(10)),
                ''.join(
                    random.choice(string.ascii_lowercase) for i in range(10)),
                Vector(''))
        ]


from models.vector import Vector
from services.service_interfaces import IRecognizer


class MockRecognizer(IRecognizer):  # TODO: обращение к серверу
    def __init__(self):
        pass

    def extract(self, picture) -> Vector:
        return Vector('asrtastsrt')

    def compare_vectors(self, user_vector: Vector,
                        extracted_vector: Vector) -> float:
        return 0.9
