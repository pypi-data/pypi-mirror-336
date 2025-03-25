import os

import pytest_argus_server


def test_version_fixture(pytester):
    """Make sure that pytest accepts our fixture."""

    # create a temporary pytest test module
    pytester.makepyfile("""
        def test_sth(argus_version):
            assert argus_version == "1.33.0"
    """)

    # run pytest with the following cmd args
    result = pytester.runpytest("--argus-version=1.33.0", "-v")

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(
        [
            "*::test_sth PASSED*",
        ]
    )

    # make sure that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_help_message(pytester):
    result = pytester.runpytest(
        "--help",
    )
    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(
        [
            "argus-server:",
            "*--argus-version=ARGUS_VERSION",
            "*Set the version of the Argus API server to run",
        ],
        consecutive=True,
    )


def test_argus_api_url_fixture_should_return_expected_url(pytester):
    """Make sure argus_api_url fixture returns the expected URL."""

    # create a temporary pytest test module
    pytester.makepyfile("""
        def test_sth(argus_api_url):
            assert argus_api_url == "http://localhost:8000/api/v2/"
    """)

    # run pytest with the following cmd args
    result = pytester.runpytest(
        "--argus-version=1.30.0",  # Because 1.33 (latest) is broken
        "-v",
    )

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(
        [
            "*::test_sth PASSED*",
        ]
    )

    # make sure that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_argus_token_should_give_api_access(pytester):
    """Make sure that argus_source_system_token returns a fixture that allows
    proper access to the API.
    """

    # create a temporary pytest test module
    pytester.makepyfile("""
        import requests
        from urllib.parse import urljoin

        def test_sth(argus_api_url, argus_source_system_token):
            response = requests.get(
                urljoin(argus_api_url, "incidents/"), 
                headers={"Authorization": f"Token {argus_source_system_token}"}
            )
            assert response.status_code == 200
    """)

    # run pytest with the following cmd args
    result = pytester.runpytest(
        "--argus-version=1.30.0",  # Because 1.33 (latest) is broken
        "-v",
    )

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(
        [
            "*::test_sth PASSED*",
        ]
    )

    # make sure that we get a '0' exit code for the testsuite
    assert result.ret == 0
