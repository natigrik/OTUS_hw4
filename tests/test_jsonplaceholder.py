import pytest
import requests
from jsonschema import validate
import random
from http import HTTPStatus


@pytest.fixture
def base_url():
    base_url_local = "https://jsonplaceholder.typicode.com"
    return base_url_local


@pytest.mark.parametrize('date_type', ['posts', 'comments', 'albums', 'photos', 'todos', 'users'])
def test_list_by_type_schema(base_url, date_type):
    res = requests.get(f"{base_url}/{date_type}")
    assert res.status_code == HTTPStatus.OK

    schema = {
        "type": "array"
    }

    validate(instance=res.json(), schema=schema)


@pytest.mark.parametrize('date_type', ['posts', 'comments', 'albums', 'photos', 'todos', 'users'])
def test_list_date_count(base_url, date_type):
    res = requests.get(f"{base_url}/{date_type}")
    assert res.status_code == HTTPStatus.OK

    if date_type in ('posts', 'albums'):
        assert len(res.json()) == 100
    elif date_type == 'comments':
        assert len(res.json()) == 500
    elif date_type == 'photos':
        assert len(res.json()) == 5000
    elif date_type == 'todos':
        assert len(res.json()) == 200
    elif date_type == 'users':
        assert len(res.json()) == 10


def test_post_by_id_schema(base_url):
    res = requests.get(f"{base_url}/posts/{random.randrange(100) + 1}")
    assert res.status_code == HTTPStatus.OK

    schema = {
        "type": "object",
        "properties": {
            "userId": {"type": "number"},
            "id": {"type": "number"},
            "title": {"type": "string"},
            "body": {"type": "string"}
        },
        "required": ["userId", "id", "title", "body"]
    }

    validate(instance=res.json(), schema=schema)


def test_post_by_post_id_schema(base_url):
    res = requests.get(f"{base_url}/posts/{random.randrange(100) + 1}/comments")
    assert res.status_code == HTTPStatus.OK

    schema = {
        "type": "array"
    }

    validate(instance=res.json(), schema=schema)


def test_comments_by_post_id_schema(base_url):
    res = requests.get(f"{base_url}/comments?postId={random.randrange(100) + 1}")
    assert res.status_code == HTTPStatus.OK

    schema = {
        "type": "array"
    }

    validate(instance=res.json(), schema=schema)


def test_post(base_url):
    res = requests.post(f"{base_url}/posts", data={'title': 'foo', 'body': 'bar', 'userId': 1})
    assert res.status_code == HTTPStatus.CREATED


def test_put(base_url):
    res = requests.put(f"{base_url}/posts/1", data={'id': 1, 'title': 'foo', 'body': 'bar', 'userId': 1})
    assert res.status_code == HTTPStatus.OK


def test_patch(base_url):
    res = requests.patch(f"{base_url}/posts/1", data={'title': 'foo'})
    assert res.status_code == HTTPStatus.OK


def test_delete(base_url):
    res = requests.delete(f"{base_url}/posts/1")
    assert res.status_code == HTTPStatus.OK
