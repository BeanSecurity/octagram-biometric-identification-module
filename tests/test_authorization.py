import unittest
from unittest import mock
from unittest.mock import patch

from models.cam import Camera
from services.service_interfaces import *
from models.vector import Vector
from models.control_point import ControlPoint
from models.user import User
from services.repository import Repository
from services.recognizer import Recognizer
# from services.ACS import AccessControlSystem
from core.authorizer import Authorizer


# class MockRepository(IRepository):
#     def __init__(self):
#         pass
#
#     def get_users(self):
#         return [User('1', Vector('1')), User('2', Vector('2')), User('3', Vector('2'))]
#
#     def get_cameras(self):
#         pass
#
#     def get_control_points(self):
#         pass
#
#
# class MockRecognizer(IRecognizer):
#     def __init__(self):
#         pass
#
#     def extract(self, picture):
#         return Vector('2')
#
#     def compare_vectors(self, user_vector: Vector, extracted_vector: Vector):
#         if user_vector.value == '2':
#             return 1
#         else:
#             return 0.1
#
#
# class MockAccessControlSystem(IAccessControlSystem):
#     def __init__(self):
#         self.opened_for = None
#
#     def open_door(self, door: ControlPoint, user: User):
#         self.opened_door = door
#         self.opened_for = user
#
#     def has_access(self, door: ControlPoint, user: User):
#         return True


class TestAuthorizer(unittest.TestCase):

    @patch("services.repository.Repository")
    @patch("services.recognizer.Recognizer")
    @patch("services.service_interfaces.IAccessControlSystem")
    def test_PermittedUser_AccessGranted(self,
                                         MockRepository: mock.MagicMock,
                                         MockRecognizer: mock.MagicMock,
                                         MockAccessControlSystem: mock.MagicMock):
        mock_acs = MockAccessControlSystem.return_value
        mock_acs.has_access.return_value = True

        mock_recognizer = MockRecognizer.return_value
        mock_recognizer.extract.return_value = Vector('1')
        mock_recognizer.compare_vectors.return_value = 1

        mock_repository = MockRepository.return_value
        mock_repository.get_users.return_value = [User('1', Vector('1'))]
        mock_repository.get_control_points.return_value = [ControlPoint('1', '1')]
        mock_repository.get_cameras.return_value = [Camera('1', ControlPoint('1', '1'))]

        authorizer = Authorizer(mock_repository, mock_recognizer, mock_acs)
        authorizer.authorize(None)
        mock_acs.open_door.assert_called()

    @patch("services.repository.Repository")
    @patch("services.recognizer.Recognizer")
    @patch("services.service_interfaces.IAccessControlSystem")
    def test_NotPermittedUser_AccessDenied(self,
                                           MockRepository: mock.MagicMock,
                                           MockRecognizer: mock.MagicMock,
                                           MockAccessControlSystem: mock.MagicMock):
        mock_acs = MockAccessControlSystem.return_value
        mock_acs.has_access.return_value = False

        mock_recognizer = MockRecognizer.return_value
        mock_recognizer.extract.return_value = Vector('1')
        mock_recognizer.compare_vectors.return_value = 1

        mock_repository = MockRepository.return_value
        mock_repository.get_users.return_value = [User('1', Vector('1'))]
        mock_repository.get_control_points.return_value = [ControlPoint('1', '1')]
        mock_repository.get_cameras.return_value = [Camera('1', ControlPoint('1', '1'))]

        authorizer = Authorizer(mock_repository, mock_recognizer, mock_acs)
        authorizer.authorize(None)
        mock_acs.open_door.assert_not_called()

    @patch("services.repository.Repository")
    @patch("services.recognizer.Recognizer")
    @patch("services.service_interfaces.IAccessControlSystem")
    def test_FaceNotRecognized_DoneNothing(self,
                                           MockRepository: mock.MagicMock,
                                           MockRecognizer: mock.MagicMock,
                                           MockAccessControlSystem: mock.MagicMock):
        mock_acs = MockAccessControlSystem.return_value
        mock_acs.has_access.return_value = True

        mock_recognizer = MockRecognizer.return_value
        mock_recognizer.extract.return_value = Vector('1')
        mock_recognizer.compare_vectors.return_value = 0

        mock_repository = MockRepository.return_value
        mock_repository.get_users.return_value = [User('1', Vector('1'))]
        mock_repository.get_control_points.return_value = [ControlPoint('1', '1')]
        mock_repository.get_cameras.return_value = [Camera('1', ControlPoint('1', '1'))]

        authorizer = Authorizer(mock_repository, mock_recognizer, mock_acs)
        authorizer.authorize(None)
        mock_acs.open_door.assert_not_called()


if __name__ == '__main__':
    unittest.main()
