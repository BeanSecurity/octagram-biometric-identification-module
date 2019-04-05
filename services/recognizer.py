from models.vector import Vector
from services.service_interfaces import IRecognizer
import requests
import logging


class Recognizer(IRecognizer):
    def __init__(self):
        self._url = "http://192.168.1.108:8086/v1/prefix/pattern/"

    def extract(self, picture) -> Vector:
        try:
            if picture is None:
                return None
            headers = {
                'Content-Type': "image/jpeg",
                'Content-Length': str(len(picture)),
            }
            req = requests.Request('POST', self._url + "extract", headers=headers)
            prep = req.prepare()
            prep.body = picture
            s = requests.Session()
            response = s.send(prep)

            if response.status_code != 200:
                if response.json()['code'] not in ['BPE-003002']:
                    logger = logging.getLogger(__name__)
                    logger.exception(response.text)
                return None

            return Vector(response.content)

        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception(e)
            return None


    def compare_vectors(self, user_vector: Vector, extracted_vector: Vector) -> float:
        try:
            response = requests.post(self._url + "compare",
                                     files=dict(bio_template=user_vector.value,
                                                bio_feature=extracted_vector.value))
            if response.status_code != 200:
                logger = logging.getLogger(__name__)
                logger.exception(response.text)
                return None
            return response.json()['score']

        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception(e)
            return None



