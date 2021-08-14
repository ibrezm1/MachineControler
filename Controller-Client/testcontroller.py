import pytest
from pytest_mock import mocker 
import controller

def test_slow_function_mocked_api_call(mocker):
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'mock_examples.main.api_call',
        return_value=5
    )

    expected = 5
    actual = slow_function()
    assert expected == actual