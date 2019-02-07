from models.vector import Vector
from services.service_interfaces import IRecognizer
import requests


class Recognizer(IRecognizer):  # TODO: обращение к серверу
    def __init__(self):
        self._url = "http://46.39.253.178:49090/v1/prefix/pattern/"  # TODO: брать из конфига

    def extract(self, picture) -> Vector:
        headers = {
            'Content-Type': "image/jpeg",
        }

        files = {
            'pic': picture
        }

        response = requests.post(self._url + "extract", headers=headers, files=files)
        # response = requests.post(self._url + "extract", headers=headers, data=picture)
        return Vector(response.text)

    def compare_vectors(self, user_vector: Vector, extracted_vector: Vector) -> float:
        response = requests.post(self._url + "compare",
                                 files=dict(bio_template=user_vector, bio_feature=extracted_vector))
        return response.text


from models.vector import Vector
from services.service_interfaces import IRecognizer


class MockRecognizer(IRecognizer):  # TODO: обращение к серверу
    def __init__(self):
        pass

    def extract(self, picture) -> Vector:
        return Vector('asrtastsrt')

    def compare_vectors(self, user_vector: Vector, extracted_vector: Vector) -> float:
        return 0.9
