import pytest


# addopts = PYTEST_ADDOPTS
# PYTEST_ADDOPTS = "--url = \"https://dog.ceo\""

def pytest_addoption(parser):
    parser.addoption(
        "--url",
        default="https://ya.ru"
        # default="https://dog.ceo"
    )

    parser.addoption(
        "--status_code",
        default=200,
    )


@pytest.fixture
def base_url(request):
    return request.config.getoption("--url")
