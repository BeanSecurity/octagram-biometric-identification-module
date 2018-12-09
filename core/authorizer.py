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

        for user in access_control_system.get_unidentified_users():
            if user.face_vector.value != '':  # проверка пустого вектора юзера
                break
            pic = access_control_system.get_user_photo(user)
            if pic is None:  # проверка наличия фото юзера
                break
            vector = recognizer.extract(pic)
            if (vector.value == '') or (vector is None): # проверка наличия вектора обработанного изображения
                break
            repository.save_user(User(user.key_id, vector))

    def authorize(self, image):
        vector = self._recognizer.extract(image)
        for user in self._repository.get_users():
            score = self._recognizer.compare_vectors(user.face_vector, vector)
            if score >= self._threshold and self._access_control_system.has_access(None, user):
                self._access_control_system.open_door(None, user)
                break

        # TODO: проверка на соответсвие камер и дверей
        # TODO: обрабатывать случай, если на камере нет лица