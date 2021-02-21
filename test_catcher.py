from datetime import date, datetime
import requests
from unittest.mock import patch, mock_open, call

from catcher import transform, url_for_date
from catcher import next_search_date
from catcher import get_data
from catcher import transform
from catcher import save

def test_next_search_date():
    start = datetime(2020, 1, 1, 12, 0)
    expected = date(2020, 1, 8)
    assert next_search_date(start) == expected

def test_url_for_date():
    expected = "https://playtomic.io/api/v1/availability?user_id=me&tenant_id=da776daf-43b3-11e8-8674-52540049669c&sport_id=PADEL&local_start_min=2020-01-01T00%3A00%3A00&local_start_max=2020-01-01T23%3A59%3A59"
    assert url_for_date(date(2020, 1, 1)) == expected

class MockResponse:
    @staticmethod
    def json():
        return {'a': 'b'}

def test_get_data(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponse()
    monkeypatch.setattr(requests, 'get', mock_get)
    data = get_data("any url")
    assert data == {'a': 'b'}

def test_transform():
    data = [
    {'resource_id': 'bdbd8388-7447-4675-b01e-7f26b2d723af',
      'slots': [
          {'duration': 90, 'price': '7.5 EUR', 'start_time': '10:30:00'}],
      'start_date': '2021-02-26'},
     
    {'resource_id': 'ffec2bf4-9914-4201-9cef-b4d1bd277b1a',
      'slots': [
          {'duration': 60, 'price': '5 EUR', 'start_time': '11:00:00'},
          {'duration': 60, 'price': '5 EUR', 'start_time': '12:00:00'}],
      'start_date': '2021-02-26'},
     
    {'resource_id': 'f9c1edd7-4c52-45ce-b5b0-755b8d73ea26',
      'slots': [
          {'duration': 60, 'price': '5 EUR', 'start_time': '12:00:00'},
          {'duration': 60, 'price': '5 EUR', 'start_time': '13:00:00'},
          {'duration': 60, 'price': '5 EUR', 'start_time': '14:00:00'}],
      'start_date': '2021-02-26'}
    ]
    expected = [
        {'name': 'Paddle 1', 'available_slots': 1},
        {'name': 'Paddle 2', 'available_slots': 2},
        {'name': 'Paddle 5', 'available_slots': 3},
    ]
    assert transform(data) == expected

def test_save():
    data = [
        {'name': 'Paddle 1', 'available_slots': 1},
        {'name': 'Paddle 2', 'available_slots': 2},
        {'name': 'Paddle 5', 'available_slots': 3},
    ]
    m = mock_open()
    with patch('builtins.open', m):
        save(data, datetime(2020, 1, 1, 12, 0))
    
    print(m.mock_calls)
    print(m().mock_calls)

    some = [
        call('sunday_paddle.txt', 'a'),
        call().__enter__(),
        call().write('01/01/2020 12:00, Paddle 1, 1\n'),
        call().write('01/01/2020 12:00, Paddle 2, 2\n'),
        call().write('01/01/2020 12:00, Paddle 5, 3\n'),
        call().write('--------------------'),
        call().write('\n'),
        call().__exit__(None, None, None),
        call()
    ]
    m.assert_has_calls(some, any_order=False)
