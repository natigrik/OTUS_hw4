import pytest
import requests
from jsonschema import validate


# получение полного списка баров
def test_list_all_schema(base_url):
    res = requests.get(base_url + "/breweries")
    assert res.status_code == 200

    schema = {
        "type": "array"
    }

    validate(instance=res.json(), schema=schema)


def test_list_all_count(base_url):
    res = requests.get(base_url + "/breweries")
    assert res.status_code == 200

    assert len(res.json()) == 20


# получение списка баров по типу
@pytest.mark.parametrize('brew_type',
                         ['micro', 'nano', 'regional', 'brewpub', 'large', 'planning', 'bar', 'contract',
                          pytest.param('proprietor', marks=pytest.mark.skip(reason="баг в коде валидации: допустимое "
                                                                                   "значение указано с опечаткой:"
                                                                                   "'proprieter'")),
                          'closed'])
def test_list_by_type_schema(base_url, brew_type):
    res = requests.get(base_url + "/breweries?by_type=" + brew_type)
    assert res.status_code == 200

    schema = {
        "type": "array"
    }

    validate(instance=res.json(), schema=schema)


# получение списка баров с указанным количеством
@pytest.mark.parametrize('per_page', ['1', '49', '50', '51', '100'])
def test_list_by_count_schema(base_url, per_page):
    res = requests.get(base_url + "/breweries?per_page=" + per_page)
    assert res.status_code == 200

    schema = {
        "type": "array"
    }

    validate(instance=res.json(), schema=schema)


@pytest.mark.parametrize('per_page', ['1', '49', '50', '51', '100'])
def test_list_by_count_count(base_url, per_page):
    res = requests.get(base_url + "/breweries?per_page=" + per_page)
    assert res.status_code == 200

    count_brew = int(per_page)
    if count_brew <= 50:
        assert len(res.json()) == count_brew
    else:
        assert len(res.json()) == 50


# получение бара по id
@pytest.mark.parametrize('brew_id', ['14-lakes-brewery-crosslake', 'epidemic-ales-concord',
                                     '10th-district-brewing-company-abington'])
def test_brew_by_id_schema(base_url, brew_id):
    res = requests.get(base_url + "/breweries/" + brew_id)
    assert res.status_code == 200

    schema = {
        "type": "object"
    }

    validate(instance=res.json(), schema=schema)


# получение бара по несуществующему id
@pytest.mark.parametrize('brew_id', ['123456', '456789'])
def test_brew_by_fake_id_status(base_url, brew_id):
    res = requests.get(base_url + "/breweries/" + brew_id)
    assert res.status_code == 404


# получение списка баров по запросу на вхождение текста
@pytest.mark.parametrize('query_text', ['brewery-crosslake', 'county_province', '5103061914', 'Oakland', 'faketext'])
def test_list_by_query_schema(base_url, query_text):
    res = requests.get(base_url + "/breweries/search?query=" + query_text)
    assert res.status_code == 200

    schema = {
        "type": "array"
    }

    validate(instance=res.json(), schema=schema)


@pytest.mark.parametrize('query_type', ['search', 'autocomplete'])
def test_list_by_fake_query(base_url, query_type):
    res = requests.get(base_url + "/breweries/" + query_type + "?query=faketext")
    assert res.status_code == 200

    assert len(res.json()) == 0


def test_autocomplete_by_fake_query(base_url):
    res = requests.get(base_url + "/breweries/autocomplete?query=faketext")
    assert res.status_code == 200

    assert len(res.json()) == 0


# получение списка баров по запросу на вхождение текста в название
@pytest.mark.parametrize('query_text', ['boss', 'dog', 'running'])
def test_autocomplete_by_query_schema(base_url, query_text):
    res = requests.get(base_url + "/breweries/autocomplete?query=" + query_text)
    assert res.status_code == 200

    schema = {
        "type": "array"
    }

    validate(instance=res.json(), schema=schema)


@pytest.mark.skip(reason="баг в реализации: по доке должно отдаваться не более 15 значений, по факту отдается больше")
@pytest.mark.parametrize('query_text', ['boss', 'dog', 'brew', 'cleve'])
def test_autocomplete_by_query_count(base_url, query_text):
    res = requests.get(base_url + "/breweries/autocomplete?query=" + query_text)
    assert res.status_code == 200

    assert len(res.json()) <= 15
