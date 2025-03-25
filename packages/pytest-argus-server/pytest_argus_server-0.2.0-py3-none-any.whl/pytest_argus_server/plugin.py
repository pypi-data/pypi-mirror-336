import os
from urllib.parse import urljoin

import pytest
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

pytest_plugins = ["pytest_docker_compose"]
TEST_SOURCE_NAME = "testsource"
TEST_SOURCE_PASSWORD = "fakef00bar"


def pytest_addoption(parser):
    group = parser.getgroup("argus-server")
    group.addoption(
        "--argus-version",
        action="store",
        dest="argus_version",
        default="latest",
        help="Set the version of the Argus API server to run",
    )


def pytest_configure(config):
    """Ensure this plugin's docker-compose file is included by default"""
    plugin_dir = os.path.dirname(__file__)
    docker_compose_file = os.path.join(plugin_dir, "docker", "docker-compose.yml")
    if config.option.docker_compose and "," in config.option.docker_compose:
        config.option.docker_compose += f",{docker_compose_file}"
    else:
        config.option.docker_compose = docker_compose_file


@pytest.fixture(scope="session")
def argus_version(request):
    version = request.config.option.argus_version
    os.environ["ARGUS_VERSION"] = version
    return version


@pytest.fixture(scope="session")
def argus_source_system_token(wait_for_argus_api, argus_api_url):
    """Returns a valid source system token for a running Argus API server"""
    request_session, container = wait_for_argus_api
    container.execute(["django-admin", "create_source", TEST_SOURCE_NAME])
    container.execute(
        ["django-admin", "setpassword", TEST_SOURCE_NAME, TEST_SOURCE_PASSWORD]
    )

    print("BASE URL: ", argus_api_url)
    login_endpoint = urljoin(argus_api_url, "auth/token/login/")
    print("LOGIN_ENDPOINT:", login_endpoint)
    response = request_session.post(
        login_endpoint,
        json={"username": "testsource", "password": TEST_SOURCE_PASSWORD},
    )
    print("Raw Argus login response:", response.text)
    response.raise_for_status()
    token = response.json().get("token", None)
    assert token, f"Failed to get token from {response.text}"

    return token


@pytest.fixture(scope="session")
def argus_api_url(wait_for_argus_api):
    """Returns an API URL base for a running Argus API server"""

    _request_session, container = wait_for_argus_api
    container.execute(["django-admin", "initial_setup"])

    service = container.network_info[0]
    argus_base_url = f"http://localhost:{service.host_port}/api/v2/"
    return argus_base_url


@pytest.fixture(scope="session")
def wait_for_argus_api(argus_version, session_scoped_container_getter):
    """Wait for an Argus API server to become responsive.

    :returns: A tuple of the request session used to test for connectivity and an
    object representing the API container instance
    """
    request_session = requests.Session()
    retries = Retry(total=5, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
    request_session.mount("http://", HTTPAdapter(max_retries=retries))

    container = session_scoped_container_getter.get("argus_api")
    service = container.network_info[0]
    argus_url = f"http://127.0.0.1:{service.host_port}/"
    print(f"Attempting to connect to {argus_url}")
    assert request_session.get(argus_url)
    return request_session, container
