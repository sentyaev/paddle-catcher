from datetime import datetime, timedelta
from pprint import pprint
import requests


def get_url(today):
    in_a_week = today + timedelta(days=6)
    url = "https://playtomic.io/api/v1/availability?user_id=me&tenant_id=da776daf-43b3-11e8-8674-52540049669c&sport_id=PADEL&local_start_min={}T00%3A00%3A00&local_start_max={}T23%3A59%3A59"
    url = url.format(in_a_week, in_a_week)
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
        result.append({'name': paddle_court_name,'count': available_slots_count})

    return result

def get_paddle_court_name(resource_id):
    return ''

def save(data, dt):
    filename = 'sunday_paddle.txt'
    dt = dt.strftime('%m/%d/%Y %H:%M')
    with(open(filename, 'a')) as f:
        for x in data:
            line = '{}, {}, {}\n'.format(dt, x['name'], x['count'])
            f.write(line)
        f.write('-'*20)
        f.write('\n')

def run():
    run_time = datetime.now()
    url = get_url(run_time.date())
    data = get_data(url)
    data = transform(data)
    save(data, run_time)


if __name__ == '__main__':
    run()