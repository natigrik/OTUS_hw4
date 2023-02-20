import pytest
import requests
from jsonschema import validate
import random

# массив со списком пород для параметризации
breeds_main = ['affenpinscher', 'african', 'airedale', 'akita', 'appenzeller', 'australian', 'basenji', 'beagle',
               'bluetick', 'borzoi', 'bouvier', 'boxer', 'brabancon', 'briard', 'buhund', 'bulldog', 'bullterrier',
               'cattledog', 'chihuahua', 'chow', 'clumber', 'cockapoo', 'collie', 'coonhound', 'corgi', 'cotondetulear',
               'dachshund', 'dalmatian', 'dane', 'deerhound', 'dhole', 'dingo', 'doberman', 'elkhound', 'entlebucher',
               'eskimo', 'finnish', 'frise', 'germanshepherd', 'greyhound', 'groenendael', 'havanese', 'hound', 'husky',
               'keeshond', 'kelpie', 'komondor', 'kuvasz', 'labradoodle', 'labrador', 'leonberg', 'lhasa', 'malamute',
               'malinois', 'maltese', 'mastiff', 'mexicanhairless', 'mix', 'mountain', 'newfoundland', 'otterhound',
               'ovcharka', 'papillon', 'pekinese', 'pembroke', 'pinscher', 'pitbull', 'pointer', 'pomeranian', 'poodle',
               'pug', 'puggle', 'pyrenees', 'redbone', 'retriever', 'ridgeback', 'rottweiler', 'saluki', 'samoyed',
               'schipperke', 'schnauzer', 'setter', 'sheepdog', 'shiba', 'shihtzu', 'spaniel', 'springer', 'stbernard',
               'terrier', 'vizsla', 'waterdog', 'weimaraner', 'whippet', 'wolfhound']


# получение полного списка пород
def test_list_all_schema(base_url):
    res = requests.get(base_url + "/api/breeds/list/all")
    assert res.status_code == 200

    schema = {
        "type": "object",
        "properties": {
            "message": {"type": "object"},
            "status": {"type": "string"},
        },
        "required": ["message", "status"]
    }

    validate(instance=res.json(), schema=schema)


# получение случайной картинки любой породы
def test_random_image_schema(base_url):
    res = requests.get(base_url + "/api/breeds/image/random")
    assert res.status_code == 200

    schema = {
        "type": "object",
        "properties": {
            "message": {"type": "string"},
            "status": {"type": "string"},
        },
        "required": ["message", "status"]
    }

    validate(instance=res.json(), schema=schema)


# получение нескольких случайных картинок любых пород
def test_some_random_image_schema(base_url):
    res = requests.get(base_url + "/api/breeds/image/random/1")
    assert res.status_code == 200

    schema = {
        "type": "object",
        "properties": {
            "message": {"type": "array"},
            "status": {"type": "string"},
        },
        "required": ["message", "status"]
    }

    validate(instance=res.json(), schema=schema)


@pytest.mark.parametrize('count_images', ['1', '49', '50', '51', '100'])
def test_some_random_image_count(base_url, count_images):
    res = requests.get(base_url + "/api/breeds/image/random/" + count_images)
    assert res.status_code == 200

    images_list = res.json()
    images = []
    for key1, value1 in images_list.items():
        if key1 == 'message':
            images = value1

    count_images1 = int(count_images)
    if count_images1 <= 50:
        assert len(images) == count_images1
    else:
        assert len(images) == 50


# получение списка картинок и списка подвидов по основной породе
@pytest.mark.parametrize('list_type', ['/images', '/list'])
def test_breed_list_schema(base_url, list_type):
    res = requests.get(base_url + "/api/breed/" + random.choice(breeds_main) + list_type)
    assert res.status_code == 200
    print(res)

    schema = {
        "type": "object",
        "properties": {
            "message": {"type": "array"},
            "status": {"type": "string"},
        },
        "required": ["message", "status"]
    }

    validate(instance=res.json(), schema=schema)


# получение случайной картинки по основной породе
def test_random_image_by_breed(base_url):
    res = requests.get(base_url + "/api/breed/" + random.choice(breeds_main) + "/images/random")
    assert res.status_code == 200

    schema = {
        "type": "object",
        "properties": {
            "message": {"type": "string"},
            "status": {"type": "string"},
            "code": {"type": "number"}
        },
        "required": ["message", "status"]
    }

    validate(instance=res.json(), schema=schema)


# получение нескольких случайных картинок по основной породе
@pytest.mark.parametrize('count_images', ['1', '50', '100'])
def test_some_random_image_schema_by_breed(base_url, count_images):
    res = requests.get(base_url + "/api/breed/" + random.choice(breeds_main) + "/images/random/" + count_images)
    assert res.status_code == 200

    schema = {
        "type": "object",
        "properties": {
            "message": {"type": "array"},
            "status": {"type": "string"},
        },
        "required": ["message", "status"]
    }

    validate(instance=res.json(), schema=schema)


# получение всех картинок по полной породе
@pytest.mark.parametrize('sub_breed', ['boston', 'english', 'french'])
def test_all_images_schema_by_full_breed(base_url, sub_breed):
    res = requests.get(base_url + "/api/breed/bulldog/" + sub_breed + "/images")
    assert res.status_code == 200

    schema = {
        "type": "object",
        "properties": {
            "message": {"type": "array"},
            "status": {"type": "string"},
            "code": {"type": "number"}
        },
        "required": ["message", "status"]
    }

    validate(instance=res.json(), schema=schema)


# получение случайной картинки по полной породе
@pytest.mark.parametrize('sub_breed', ['american', 'australian', 'bedlington', 'border', 'cairn'])
def test_random_image_schema_by_full_breed(base_url, sub_breed):
    res = requests.get(base_url + "/api/breed/terrier/" + sub_breed + "/images/random")
    assert res.status_code == 200

    schema = {
        "type": "object",
        "properties": {
            "message": {"type": "string"},
            "status": {"type": "string"},
        },
        "required": ["message", "status"]
    }

    validate(instance=res.json(), schema=schema)


# получение нескольких случайных картинок по полной породе
@pytest.mark.parametrize('sub_breed', ['chesapeake', 'curly', 'flatcoated', 'golden'])
@pytest.mark.parametrize('count_images', ['1', '50', '100'])
def test_some_random_image_schema_by_full_breed(base_url, count_images, sub_breed):
    res = requests.get(base_url + "/api/breed/retriever/" + sub_breed + "/images/random/" + count_images)
    assert res.status_code == 200

    schema = {
        "type": "object",
        "properties": {
            "message": {"type": "array"},
            "status": {"type": "string"},
        },
        "required": ["message", "status"]
    }

    validate(instance=res.json(), schema=schema)
