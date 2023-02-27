import pytest
import requests
from jsonschema import validate
import random
from http import HTTPStatus


@pytest.fixture
def base_url():
    base_url_local = "https://dog.ceo"
    return base_url_local


"""массив со списком пород для параметризации"""
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


def test_list_all_schema(base_url):
    """получение полного списка пород"""
    res = requests.get(base_url + "/api/breeds/list/all")
    assert res.status_code == HTTPStatus.OK

    schema = {
        "type": "object",
        "properties": {
            "message": {"type": "object"},
            "status": {"type": "string"},
        },
        "required": ["message", "status"]
    }

    validate(instance=res.json(), schema=schema)


def test_random_image_schema(base_url):
    """получение случайной картинки любой породы"""
    res = requests.get(base_url + "/api/breeds/image/random")
    assert res.status_code == HTTPStatus.OK

    schema = {
        "type": "object",
        "properties": {
            "message": {"type": "string"},
            "status": {"type": "string"},
        },
        "required": ["message", "status"]
    }

    validate(instance=res.json(), schema=schema)


def test_some_random_image_schema(base_url):
    """получение нескольких случайных картинок любых пород"""
    res = requests.get(base_url + "/api/breeds/image/random/1")
    assert res.status_code == HTTPStatus.OK

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
    res = requests.get(f"{base_url}/api/breeds/image/random/{count_images}")
    exp_images_count = count_images if int(count_images) <= 50 else 50
    assert res.status_code == HTTPStatus.OK

    images_list = res.json()

    assert 'message' in images_list
    images = images_list['message']
    assert len(images) == int(exp_images_count)


@pytest.mark.parametrize('list_type', ['/images', '/list'])
def test_breed_list_schema(base_url, list_type):
    """получение списка картинок и списка подвидов по основной породе"""
    res = requests.get(f"{base_url}/api/breed/{random.choice(breeds_main)}{list_type}")
    assert res.status_code == HTTPStatus.OK
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


def test_random_image_by_breed(base_url):
    """получение случайной картинки по основной породе"""
    res = requests.get(f"{base_url}/api/breed/{random.choice(breeds_main)}/images/random")
    assert res.status_code == HTTPStatus.OK

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


@pytest.mark.parametrize('count_images', ['1', '50', '100'])
def test_some_random_image_schema_by_breed(base_url, count_images):
    """получение нескольких случайных картинок по основной породе"""
    res = requests.get(f"{base_url}/api/breed/{random.choice(breeds_main)}/images/random/{count_images}")
    assert res.status_code == HTTPStatus.OK

    schema = {
        "type": "object",
        "properties": {
            "message": {"type": "array"},
            "status": {"type": "string"},
        },
        "required": ["message", "status"]
    }

    validate(instance=res.json(), schema=schema)


@pytest.mark.parametrize('sub_breed', ['boston', 'english', 'french'])
def test_all_images_schema_by_full_breed(base_url, sub_breed):
    """получение всех картинок по полной породе"""
    res = requests.get(f"{base_url}/api/breed/bulldog/{sub_breed}/images")
    assert res.status_code == HTTPStatus.OK

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


@pytest.mark.parametrize('sub_breed', ['american', 'australian', 'bedlington', 'border', 'cairn'])
def test_random_image_schema_by_full_breed(base_url, sub_breed):
    """получение случайной картинки по полной породе"""
    res = requests.get(f"{base_url}/api/breed/terrier/{sub_breed}/images/random")
    assert res.status_code == HTTPStatus.OK

    schema = {
        "type": "object",
        "properties": {
            "message": {"type": "string"},
            "status": {"type": "string"},
        },
        "required": ["message", "status"]
    }

    validate(instance=res.json(), schema=schema)


@pytest.mark.parametrize('sub_breed', ['chesapeake', 'curly', 'flatcoated', 'golden'])
@pytest.mark.parametrize('count_images', ['1', '50', '100'])
def test_some_random_image_schema_by_full_breed(base_url, count_images, sub_breed):
    """получение нескольких случайных картинок по полной породе"""
    res = requests.get(f"{base_url}/api/breed/retriever/{sub_breed}/images/random/{count_images}")
    assert res.status_code == HTTPStatus.OK

    schema = {
        "type": "object",
        "properties": {
            "message": {"type": "array"},
            "status": {"type": "string"},
        },
        "required": ["message", "status"]
    }

    validate(instance=res.json(), schema=schema)
