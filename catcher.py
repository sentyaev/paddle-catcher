from datetime import datetime, timedelta
from pprint import pprint
import requests


def next_search_date(start):
    in_a_week = start.date() + timedelta(days=7)
    return in_a_week

def url_for_date(search_date):
    url = "https://playtomic.io/api/v1/availability?user_id=me&tenant_id=da776daf-43b3-11e8-8674-52540049669c&sport_id=PADEL&local_start_min={}T00%3A00%3A00&local_start_max={}T23%3A59%3A59"
    url = url.format(search_date, search_date)
    return url

def get_data(url):
    data = requests.get(url)
    return data.json()

def transform(data):
    # [
    #  {'resource_id': 'f457dda9-3a49-455b-91cb-f6dd47f412bd',
    #   'slots': [{'duration': 90, 'price': '7.5 EUR', 'start_time': '10:30:00'}],
    #   'start_date': '2021-02-26'},
    #  
    # {'resource_id': '91c341b0-bbc2-4671-9c54-8ddf8816a0d1',
    #   'slots': [{'duration': 60, 'price': '5 EUR', 'start_time': '11:00:00'}],
    #   'start_date': '2021-02-26'},
    #  
    # {'resource_id': 'bdbd8388-7447-4675-b01e-7f26b2d723af',
    #   'slots': [{'duration': 60, 'price': '5 EUR', 'start_time': '12:00:00'}],
    #   'start_date': '2021-02-26'}
    # ]
    result = []
    for element in data:
        resource_id = element['resource_id']
        paddle_court_name = get_paddle_court_name(resource_id)
        slots = element['slots']
        available_slots_count = len(slots)
        result.append({'name': paddle_court_name,'available_slots': available_slots_count})

    return result

# 'bdbd8388-7447-4675-b01e-7f26b2d723af' = 'paddle 1',
# 'ffec2bf4-9914-4201-9cef-b4d1bd277b1a' = 'paddle 2',
# 'f457dda9-3a49-455b-91cb-f6dd47f412bd' = 'paddle 3',
# '91c341b0-bbc2-4671-9c54-8ddf8816a0d1' = 'paddle 4',
# 'f9c1edd7-4c52-45ce-b5b0-755b8d73ea26' = 'paddle 5',

def get_paddle_court_name(resource_id):
    paddle_name = ''
    if resource_id == 'bdbd8388-7447-4675-b01e-7f26b2d723af':
        paddle_name = 'Paddle 1'
    elif resource_id == 'ffec2bf4-9914-4201-9cef-b4d1bd277b1a':
        paddle_name = 'Paddle 2'
    elif resource_id == 'f457dda9-3a49-455b-91cb-f6dd47f412bd':
        paddle_name = 'Paddle 3'
    elif resource_id == '91c341b0-bbc2-4671-9c54-8ddf8816a0d1':
        paddle_name = 'Paddle 4'
    elif resource_id == 'f9c1edd7-4c52-45ce-b5b0-755b8d73ea26':
        paddle_name = 'Paddle 5'
    
    return paddle_name

def save(data, dt):
    filename = 'sunday_paddle.txt'
    dt_str = dt.strftime('%m/%d/%Y %H:%M')
    with(open(filename, 'a')) as f:
        for x in data:
            line = '{}, {}, {}\n'.format(dt_str, x['name'], x['available_slots'])
            f.write(line)
        f.write('-'*20)
        f.write('\n')

def run():
    run_time = datetime.now()
    next_search = next_search_date(run_time)
    url = url_for_date(next_search)
    data = get_data(url)
    data = transform(data)
    save(data, run_time)


if __name__ == '__main__':
    run()