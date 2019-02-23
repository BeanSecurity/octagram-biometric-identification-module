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



class TestAuthorization(unittest.TestCase):

    @patch("services.repository.IRepository")
    @patch("services.recognizer.IRecognizer")
    @patch("services.service_interfaces.IAccessControlSystem")
    def test_SomePermittedUsers_DoorOpenOnce(self,
                                             MockRepository: mock.MagicMock,
                                             MockRecognizer: mock.MagicMock,
                                             MockAccessControlSystem: mock.MagicMock):
        mock_acs = MockAccessControlSystem.return_value
        mock_acs.has_access.return_value = True

        mock_recognizer = MockRecognizer.return_value
        mock_recognizer.extract.return_value = Vector('1')
        mock_recognizer.compare_vectors.return_value = 1

        mock_repository = MockRepository.return_value
        mock_repository.get_users.return_value = [User('1', Vector('1'), ''),
                                                  User('2', Vector('2'), ''),
                                                  User('3', Vector('3'), '')]
        mock_repository.get_control_points.return_value = [ControlPoint('1', '1')]
        mock_repository.get_cameras.return_value = [Camera('1', ControlPoint('1', '1'))]

        authorizer = Authorizer(mock_repository, mock_recognizer, mock_acs)
        authorizer.authorize(None)
        mock_acs.open_door.assert_called_once()

    @patch("services.repository.IRepository")
    @patch("services.recognizer.IRecognizer")
    @patch("services.service_interfaces.IAccessControlSystem")
    def test_PermittedUser_OpenDoor(self,
                                    MockRepository: mock.MagicMock,
                                    MockRecognizer: mock.MagicMock,
                                    MockAccessControlSystem: mock.MagicMock):
        mock_acs = MockAccessControlSystem.return_value
        mock_acs.has_access.return_value = True

        mock_recognizer = MockRecognizer.return_value
        mock_recognizer.extract.return_value = Vector('1')
        mock_recognizer.compare_vectors.return_value = 1

        mock_repository = MockRepository.return_value
        mock_repository.get_users.return_value = [User('1', Vector('1'), '')]
        mock_repository.get_control_points.return_value = [ControlPoint('1', '1')]
        mock_repository.get_cameras.return_value = [Camera('1', ControlPoint('1', '1'))]

        authorizer = Authorizer(mock_repository, mock_recognizer, mock_acs)
        authorizer.authorize(None)
        mock_acs.open_door.assert_called()

    @patch("services.repository.IRepository")
    @patch("services.recognizer.IRecognizer")
    @patch("services.service_interfaces.IAccessControlSystem")
    def test_NotPermittedUser_DoNothing(self,
                                        MockRepository: mock.MagicMock,
                                        MockRecognizer: mock.MagicMock,
                                        MockAccessControlSystem: mock.MagicMock):
        mock_acs = MockAccessControlSystem.return_value
        mock_acs.has_access.return_value = False

        mock_recognizer = MockRecognizer.return_value
        mock_recognizer.extract.return_value = Vector('1')
        mock_recognizer.compare_vectors.return_value = 1

        mock_repository = MockRepository.return_value
        mock_repository.get_users.return_value = [User('1', Vector('1'), '')]
        mock_repository.get_control_points.return_value = [ControlPoint('1', '1')]
        mock_repository.get_cameras.return_value = [Camera('1', ControlPoint('1', '1'))]

        authorizer = Authorizer(mock_repository, mock_recognizer, mock_acs)
        authorizer.authorize(None)
        mock_acs.open_door.assert_not_called()

    @patch("services.repository.IRepository")
    @patch("services.recognizer.IRecognizer")
    @patch("services.service_interfaces.IAccessControlSystem")
    def test_FaceNotRecognized_DoNothing(self,
                                         MockRepository: mock.MagicMock,
                                         MockRecognizer: mock.MagicMock,
                                         MockAccessControlSystem: mock.MagicMock):
        mock_acs = MockAccessControlSystem.return_value
        mock_acs.has_access.return_value = True

        mock_recognizer = MockRecognizer.return_value
        mock_recognizer.extract.return_value = Vector('1')
        mock_recognizer.compare_vectors.return_value = 0

        mock_repository = MockRepository.return_value
        mock_repository.get_users.return_value = [User('1', Vector('1'), '')]
        mock_repository.get_control_points.return_value = [ControlPoint('1', '1')]
        mock_repository.get_cameras.return_value = [Camera('1', ControlPoint('1', '1'))]

        authorizer = Authorizer(mock_repository, mock_recognizer, mock_acs)
        authorizer.authorize(None)
        mock_acs.open_door.assert_not_called()

    @patch("services.repository.IRepository")
    @patch("services.recognizer.IRecognizer")
    @patch("services.service_interfaces.IAccessControlSystem")
    def test_NoUsers_DoNothing(self,
                               MockRepository: mock.MagicMock,
                               MockRecognizer: mock.MagicMock,
                               MockAccessControlSystem: mock.MagicMock):
        mock_acs = MockAccessControlSystem.return_value
        mock_acs.has_access.return_value = True

        mock_recognizer = MockRecognizer.return_value
        mock_recognizer.extract.return_value = Vector('1')
        mock_recognizer.compare_vectors.return_value = 1

        mock_repository = MockRepository.return_value
        mock_repository.get_users.return_value = []
        mock_repository.get_control_points.return_value = [ControlPoint('1', '1')]
        mock_repository.get_cameras.return_value = [Camera('1', ControlPoint('1', '1'))]

        authorizer = Authorizer(mock_repository, mock_recognizer, mock_acs)
        authorizer.authorize(None)
        mock_acs.open_door.assert_not_called()

    @patch("services.repository.IRepository")
    @patch("services.recognizer.IRecognizer")
    @patch("services.service_interfaces.IAccessControlSystem")
    def test_ScoreIsLowerThanThreshold_DoNoting(self,
                                                MockRepository: mock.MagicMock,
                                                MockRecognizer: mock.MagicMock,
                                                MockAccessControlSystem: mock.MagicMock):
        mock_acs = MockAccessControlSystem.return_value
        mock_acs.has_access.return_value = True

        mock_recognizer = MockRecognizer.return_value
        mock_recognizer.extract.return_value = Vector('1')

        mock_repository = MockRepository.return_value
        mock_repository.get_users.return_value = [User('1', Vector('1'), '')]
        mock_repository.get_control_points.return_value = [ControlPoint('1', '1')]
        mock_repository.get_cameras.return_value = [Camera('1', ControlPoint('1', '1'))]

        authorizer = Authorizer(mock_repository, mock_recognizer, mock_acs)
        mock_recognizer.compare_vectors.return_value = authorizer._threshold - 0.0000000001
        authorizer.authorize(None)
        mock_acs.open_door.assert_not_called()

    @patch("services.repository.IRepository")
    @patch("services.recognizer.IRecognizer")
    @patch("services.service_interfaces.IAccessControlSystem")
    def test_ScoreIsEqualToThreshold_OpenDoor(self,
                                              MockRepository: mock.MagicMock,
                                              MockRecognizer: mock.MagicMock,
                                              MockAccessControlSystem: mock.MagicMock):
        mock_acs = MockAccessControlSystem.return_value
        mock_acs.has_access.return_value = True

        mock_recognizer = MockRecognizer.return_value
        mock_recognizer.extract.return_value = Vector('1')

        mock_repository = MockRepository.return_value
        mock_repository.get_users.return_value = [User('1', Vector('1'), '')]
        mock_repository.get_control_points.return_value = [ControlPoint('1', '1')]
        mock_repository.get_cameras.return_value = [Camera('1', ControlPoint('1', '1'))]

        authorizer = Authorizer(mock_repository, mock_recognizer, mock_acs)
        mock_recognizer.compare_vectors.return_value = authorizer._threshold
        authorizer.authorize(None)
        mock_acs.open_door.assert_called()

    @patch("services.repository.IRepository")
    @patch("services.recognizer.IRecognizer")
    @patch("services.service_interfaces.IAccessControlSystem")
    def test_ScoreIsHigherThanThreshold_DoNoting(self,
                                                 MockRepository: mock.MagicMock,
                                                 MockRecognizer: mock.MagicMock,
                                                 MockAccessControlSystem: mock.MagicMock):
        mock_acs = MockAccessControlSystem.return_value
        mock_acs.has_access.return_value = True

        mock_recognizer = MockRecognizer.return_value
        mock_recognizer.extract.return_value = Vector('1')

        mock_repository = MockRepository.return_value
        mock_repository.get_users.return_value = [User('1', Vector('1'), '')]
        mock_repository.get_control_points.return_value = [ControlPoint('1', '1')]
        mock_repository.get_cameras.return_value = [Camera('1', ControlPoint('1', '1'))]

        authorizer = Authorizer(mock_repository, mock_recognizer, mock_acs)
        mock_recognizer.compare_vectors.return_value = authorizer._threshold + 0.0000000001
        authorizer.authorize(None)
        mock_acs.open_door.assert_called()

    @patch("services.repository.IRepository")
    @patch("services.recognizer.IRecognizer")
    @patch("services.service_interfaces.IAccessControlSystem")
    def test_VectorIsNone_DoNoting(self,
                                   MockRepository: mock.MagicMock,
                                   MockRecognizer: mock.MagicMock,
                                   MockAccessControlSystem: mock.MagicMock):
        mock_acs = MockAccessControlSystem.return_value
        mock_acs.has_access.return_value = True

        mock_recognizer = MockRecognizer.return_value
        mock_recognizer.extract.return_value = None
        mock_recognizer.compare_vectors.return_value = 1

        mock_repository = MockRepository.return_value
        mock_repository.get_users.return_value = [User('1', Vector('1'), '')]
        mock_repository.get_control_points.return_value = [ControlPoint('1', '1')]
        mock_repository.get_cameras.return_value = [Camera('1', ControlPoint('1', '1'))]

        authorizer = Authorizer(mock_repository, mock_recognizer, mock_acs)

        authorizer.authorize(None)
        mock_acs.open_door.assert_not_called()

    @patch("services.repository.IRepository")
    @patch("services.recognizer.IRecognizer")
    @patch("services.service_interfaces.IAccessControlSystem")
    def test_UsersIsNone_DoNoting(self,
                                  MockRepository: mock.MagicMock,
                                  MockRecognizer: mock.MagicMock,
                                  MockAccessControlSystem: mock.MagicMock):
        mock_acs = MockAccessControlSystem.return_value
        mock_acs.has_access.return_value = True

        mock_recognizer = MockRecognizer.return_value
        mock_recognizer.extract.return_value = Vector('1')
        mock_recognizer.compare_vectors.return_value = 1

        mock_repository = MockRepository.return_value
        mock_repository.get_users.return_value = None
        mock_repository.get_control_points.return_value = [ControlPoint('1', '1')]
        mock_repository.get_cameras.return_value = [Camera('1', ControlPoint('1', '1'))]

        authorizer = Authorizer(mock_repository, mock_recognizer, mock_acs)

        authorizer.authorize(None)
        mock_acs.open_door.assert_not_called()

    @patch("services.repository.IRepository")
    @patch("services.recognizer.IRecognizer")
    @patch("services.service_interfaces.IAccessControlSystem")
    def test_ScoreIsNone_DoNoting(self,
                                  MockRepository: mock.MagicMock,
                                  MockRecognizer: mock.MagicMock,
                                  MockAccessControlSystem: mock.MagicMock):
        mock_acs = MockAccessControlSystem.return_value
        mock_acs.has_access.return_value = True

        mock_recognizer = MockRecognizer.return_value
        mock_recognizer.extract.return_value = Vector('1')
        mock_recognizer.compare_vectors.return_value = None

        mock_repository = MockRepository.return_value
        mock_repository.get_users.return_value = [User('1', Vector('1'), '')]
        mock_repository.get_control_points.return_value = [ControlPoint('1', '1')]
        mock_repository.get_cameras.return_value = [Camera('1', ControlPoint('1', '1'))]

        authorizer = Authorizer(mock_repository, mock_recognizer, mock_acs)
        authorizer.authorize(None)
        mock_acs.open_door.assert_not_called()

    @patch("services.repository.IRepository")
    @patch("services.recognizer.IRecognizer")
    @patch("services.service_interfaces.IAccessControlSystem")
    def test_OneScoreIsNone_ContinueAuthorization(self,
                                                  MockRepository: mock.MagicMock,
                                                  MockRecognizer: mock.MagicMock,
                                                  MockAccessControlSystem: mock.MagicMock):
        mock_acs = MockAccessControlSystem.return_value
        mock_acs.has_access.return_value = True

        mock_recognizer = MockRecognizer.return_value
        mock_recognizer.extract.return_value = Vector('1')
        mock_recognizer.compare_vectors.side_effect = [None, 1]

        mock_repository = MockRepository.return_value
        mock_repository.get_users.return_value = [User('1', Vector('1'), ''),
                                                  User('2', Vector('2'), '')]
        mock_repository.get_control_points.return_value = [ControlPoint('1', '1')]
        mock_repository.get_cameras.return_value = [Camera('1', ControlPoint('1', '1'))]

        authorizer = Authorizer(mock_repository, mock_recognizer, mock_acs)
        authorizer.authorize(None)
        mock_acs.open_door.assert_called()


if __name__ == '__main__':
    unittest.main()
