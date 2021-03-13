import sys
from io import BytesIO  # Этот класс поможет нам сделать картинку из потока байт
from samples.geocoder import geocode, get_ll_span
import requests
from PIL import Image


def search(toponym_to_find):
    toponym = geocode(toponym_to_find)
    ll, spn = get_ll_span(toponym)

    # Собираем параметры для запроса к StaticMapsAPI:
    map_params = {
        "ll": ll,
        "spn": spn,
        "l": "map",
        "pt": f"{ll},comma"
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    # ... и выполняем запрос
    response = requests.get(map_api_server, params=map_params)

    return BytesIO(response.content)
