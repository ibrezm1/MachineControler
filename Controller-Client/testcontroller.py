import pytest
from pytest_mock import mocker
import controller
import cv2 as cv
from controller import Bot
import requests_mock
import requests
import mock


def test_botObserve(mocker):
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'controller.url_to_image',
        return_value=cv.imread('images/notify.png')
    )
    bot1 = Bot('http://dummyserver', 0.8, 60)
    expected = True
    actual = bot1.botObserve((1, 2, 3, 4), 'images/notify.png')
    assert expected == actual


def test_notify(requests_mock):
    requests_mock.get('http://dummyserver/play', text='data')
    bot1 = Bot('http://dummyserver', 0.8, 60)
    bot1.botNotify()
    assert requests_mock.called == True
    assert requests_mock.call_count == 1


def test_botAct(mocker, requests_mock):
    requests_mock.get('http://dummyserver/mouse', text='data')
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'controller.url_to_image',
        return_value=cv.imread('images/notify.png')
    )
    bot1 = Bot('http://dummyserver', 0.8, 60)
    expected = True
    bot1.botObserve((1, 2, 3, 4), 'images/notify.png')
    bot1.botAct()
    assert requests_mock.call_count == 1


def test_botRespond(mocker, requests_mock):
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'controller.Bot.botObserve',
        return_value=True
    )
    mocker_notify = mocker.patch(
        # api_call is from slow.py but imported to main.py
        'controller.Bot.botNotify',
        return_value=True
    )
    mocker_act= mocker.patch(
        # api_call is from slow.py but imported to main.py
        'controller.Bot.botAct',
        return_value=True
    )
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'controller.Bot.botisUserinActive',
        return_value=True
    )
    bot1 = Bot('http://dummyserver', 0.8, 60)
    region = {'region':[1,2,3,4],'matchimage':'images/OK-15mins-wait.png', 'check': 'match', 'validateisactive': True,
              'notify': True, 'action': 'click'}
    bot1.botRespond(region) 
    mocker_notify.assert_called_with()
    mocker_act.assert_called_with()