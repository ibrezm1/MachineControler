import pytest
from pytest_mock import mocker 
import controller
import cv2 as cv
from controller import Bot
import requests_mock
import requests

def test_botObserve(mocker):
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'controller.url_to_image',
        return_value=cv.imread('images/notify.png')
    )
    bot1 = Bot('dummyserver', 0.8, 60)
    expected = True
    actual = bot1.botObserve((1,2,3,4),'images/notify.png')
    assert expected == actual
    
def test_notify(requests_mock):
    requests_mock.get('http://test.com', text='data')
    bot1 = Bot('dummyserver', 0.8, 60)
    expected = 'data'
    actual = requests.get('http://test.com').text
    assert expected == actual
    assert requests_mock.called == True
    assert requests_mock.call_count == 1

def test_botAct(mocker,requests_mock):
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'controller.url_to_image',
        return_value=cv.imread('images/notify.png')
    )
    bot1 = Bot('dummyserver', 0.8, 60)
    expected = True
    actual = bot1.botObserve((1,2,3,4),'images/notify.png')
    assert expected == actual
    requests_mock.get('http://test.com', text='data')