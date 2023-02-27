import pytest
import requests
from jsonschema import validate
from http import HTTPStatus


@pytest.fixture
def base_url():
    base_url_local = "https://api.openbrewerydb.org"
    return base_url_local


def test_list_all_schema(base_url):
    """получение полного списка баров"""
    res = requests.get(base_url + "/breweries")
    assert res.status_code == HTTPStatus.OK

    schema = {
        "type": "array"
    }

    validate(instance=res.json(), schema=schema)


def test_list_all_count(base_url):
    res = requests.get(base_url + "/breweries")
    assert res.status_code == HTTPStatus.OK

    assert len(res.json()) == 20


@pytest.mark.parametrize('brew_type',
                         ['micro', 'nano', 'regional', 'brewpub', 'large', 'planning', 'bar', 'contract',
                          pytest.param('proprietor', marks=pytest.mark.skip(reason="баг в коде валидации: допустимое "
                                                                                   "значение указано с опечаткой:"
                                                                                   "'proprieter'")),
                          'closed'])
def test_list_by_type_schema(base_url, brew_type):
    """получение списка баров по типу"""
    res = requests.get(f"{base_url}/breweries?by_type={brew_type}")
    assert res.status_code == HTTPStatus.OK

    schema = {
        "type": "array"
    }

    validate(instance=res.json(), schema=schema)


@pytest.mark.parametrize('per_page', ['1', '49', '50', '51', '100'])
def test_list_by_count_schema(base_url, per_page):
    """получение списка баров с указанным количеством"""
    res = requests.get(f"{base_url}/breweries?per_page={per_page}")
    assert res.status_code == HTTPStatus.OK

    schema = {
        "type": "array"
    }

    validate(instance=res.json(), schema=schema)


@pytest.mark.parametrize('per_page', ['1', '49', '50', '51', '100'])
def test_list_by_count_count(base_url, per_page):
    """получение списка баров с указанным количеством"""
    res = requests.get(f"{base_url}/breweries?per_page={per_page}")
    assert res.status_code == HTTPStatus.OK

    exp_count_brew = per_page if int(per_page) <= 50 else 50
    assert len(res.json()) == int(exp_count_brew)


@pytest.mark.parametrize('brew_id', ['14-lakes-brewery-crosslake', 'epidemic-ales-concord',
                                     '10th-district-brewing-company-abington'])
def test_brew_by_id_schema(base_url, brew_id):
    """получение бара по id"""
    res = requests.get(f"{base_url}/breweries/{brew_id}")
    assert res.status_code == HTTPStatus.OK

    schema = {
        "type": "object"
    }

    validate(instance=res.json(), schema=schema)


@pytest.mark.parametrize('brew_id', ['123456', '456789'])
def test_brew_by_fake_id_status(base_url, brew_id):
    """получение бара по несуществующему id"""
    res = requests.get(f"{base_url}/breweries/{brew_id}")
    assert res.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize('query_text', ['brewery-crosslake', 'county_province', '5103061914', 'Oakland', 'faketext'])
def test_list_by_query_schema(base_url, query_text):
    """получение списка баров по запросу на вхождение текста"""
    res = requests.get(f"{base_url}/breweries/search?query={query_text}")
    assert res.status_code == HTTPStatus.OK

    schema = {
        "type": "array"
    }

    validate(instance=res.json(), schema=schema)


@pytest.mark.parametrize('query_type', ['search', 'autocomplete'])
def test_by_fake_query(base_url, query_type):
    res = requests.get(f"{base_url}/breweries/{query_type}?query=faketext")
    assert res.status_code == HTTPStatus.OK

    assert len(res.json()) == 0


@pytest.mark.parametrize('query_text', ['boss', 'dog', 'running'])
def test_autocomplete_by_query_schema(base_url, query_text):
    """получение списка баров по запросу на вхождение текста в название"""
    res = requests.get(f"{base_url}/breweries/autocomplete?query={query_text}")
    assert res.status_code == HTTPStatus.OK

    schema = {
        "type": "array"
    }

    validate(instance=res.json(), schema=schema)


@pytest.mark.skip(reason="баг в реализации: по доке должно отдаваться не более 15 значений, по факту отдается больше")
@pytest.mark.parametrize('query_text', ['boss', 'dog', 'brew', 'cleve'])
def test_autocomplete_by_query_count(base_url, query_text):
    res = requests.get(f"{base_url}/breweries/autocomplete?query={query_text}")
    assert res.status_code == HTTPStatus.OK

    assert len(res.json()) <= 15
