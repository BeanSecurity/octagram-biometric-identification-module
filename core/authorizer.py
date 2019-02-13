from services.service_interfaces import *
from models.control_point import ControlPoint
from services.repository import Repository


class Authorizer(IAuthorizer):

    def __init__(self, repository: IRepository, recognizer: IRecognizer,
                 access_control_system: IAccessControlSystem):
        self._repository = repository
        self._recognizer = recognizer
        self._access_control_system = access_control_system
        self._threshold = 0.7

        users = access_control_system.get_unidentified_users()
        if users is None:
            return

        for user in users:
            pic = access_control_system.get_user_photo(user)
            if pic is None:  # проверка наличия фото юзера
                continue
            vector = recognizer.extract(pic)
            if (vector is None) or (vector.value == ''):  # проверка наличия вектора обработанного изображения
                continue
            repository.save_user(User(user.key_id, user.full_name, vector))

    def authorize(self, image):

        vector = self._recognizer.extract(image)
        if vector is None or vector == '':
            return

        users = self._repository.get_users()
        if users is None:
            return

        for user in users:
            score = self._recognizer.compare_vectors(user.face_vector, vector)
            if score is None:
                continue
            elif score >= self._threshold and self._access_control_system.has_access(None, user):
                self._access_control_system.open_door(None, user)
                break

        # TODO: проверка на соответсвие камер и дверей
        # TODO: обрабатывать случай, если на камере нет лица