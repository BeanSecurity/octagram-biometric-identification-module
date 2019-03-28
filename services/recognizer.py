from models.vector import Vector
from services.service_interfaces import IRecognizer
import requests
import logging


class Recognizer(IRecognizer):  # TODO: обращение к серверу
    def __init__(self):
        self._url = "http://192.168.1.108:8086/v1/prefix/pattern/"  # TODO: брать из конфига

    def extract(self, picture) -> Vector:
        try:
            headers = {
                'Content-Type': "image/jpeg",
                'Content-Length': str(len(picture)),
            }
            req = requests.Request('POST', self._url + "extract", headers=headers)
            prep = req.prepare()
            prep.body = picture
            s = requests.Session()
            response = s.send(prep)
            logger = logging.getLogger(__name__)
            logger.debug(response.text)

        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception(e)
            return None

        if response.status_code != 200:
            logger = logging.getLogger(__name__)
            logger.debug(response.text)
            return None

        return Vector(response.text)

    def compare_vectors(self, user_vector: Vector, extracted_vector: Vector) -> float:
        try:
            response = requests.post(self._url + "compare",
                                     files=dict(bio_template=user_vector,
                                                bio_feature=extracted_vector))
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception(e)
            return None

        if response.status_code != 200:
            logger = logging.getLogger(__name__)
            logger.debug(response.text)
            return None

        return response.text


