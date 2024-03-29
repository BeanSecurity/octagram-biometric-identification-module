from services.service_interfaces import *
from models.control_point import ControlPoint
from services.repository import Repository
import logging


class Authorizer(IAuthorizer):
    def __init__(self, repository: IRepository, recognizer: IRecognizer,
                 access_control_system: IAccessControlSystem):
        self._repository = repository
        self._recognizer = recognizer
        self._access_control_system = access_control_system
        self._threshold = 0.7

        users = access_control_system.get_unidentified_users()

        logger = logging.getLogger(__name__)
        logger.info('Users: ' + str(users))

        if users is None:
            return

        for user in users:
            logger = logging.getLogger(__name__)
            logger.debug('Initial extracting user: ' + str(user))

            pic = access_control_system.get_user_photo(user)

            # проверка наличия фото юзера
            if pic is None:
                logger.info('Photo is not found for user: ' + str(user))
                continue

            logger.info('Extracting user photo: ' + str(user))
            vector = recognizer.extract(pic)

            # проверка наличия вектора обработанного изображения
            if (vector is None) or (vector.value == ''):
                logger.info('Face on photo is not found for user: ' + str(user))
                continue

            repository.save_user(User(user.key_id, user.full_name, vector))
            logger.info('Save face vector for user: ' + str(user))

    def authorize(self, image):

        vector = self._recognizer.extract(image)
        if vector is None or vector == '':
            return

        logger = logging.getLogger(__name__)
        logger.info('Face detected on camera')

        users = self._repository.get_users()
        if users is None:
            return

        for user in users:
            score = self._recognizer.compare_vectors(user.face_vector, vector)
            if score is None:
                continue

            logger = logging.getLogger(__name__)
            logger.debug('User('+str(user)+') check with score: '+str(score))

            if score >= self._threshold and self._access_control_system.has_access(
                    None, user):
                self._access_control_system.open_door(None, user)
                logger = logging.getLogger(__name__)
                logger.info('Door opened for: {} with score - {}'.format(
                    user, score))
                return

        logger.info('No matches for face on camera')
