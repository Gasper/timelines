
import datetime
import random
import uuid

def generate_categories():
    return [
        {'id': 'sport-category', 'name': 'Sport'},
        {'id': 'politics-category', 'name': 'Politics'},
        {'id': 'religion-category', 'name': 'Religion'},
        {'id': 'music-category', 'name': 'Music'}
    ]

def generate_groups():
    return [
        {'id': 'tdf-2020', 'category_id': 'sport-category', 'name': 'Tour de France 2020'},
        {'id': 'oi-2021', 'category_id': 'sport-category', 'name': 'Tokio Olympics 2021'},
        {'id': 'pl-2020', 'category_id': 'sport-category', 'name': 'Premier League 2020-2021'},
        {'id': 'lavuelta-2020', 'category_id': 'sport-category', 'name': 'La Vuelta 2020'},

        {'id': 'politics1', 'category_id': 'politics-category', 'name': 'Politics 1'},
        {'id': 'politics2', 'category_id': 'politics-category', 'name': 'Politics 2'},
        {'id': 'politics3', 'category_id': 'politics-category', 'name': 'Politics 3'},
        {'id': 'politics4', 'category_id': 'politics-category', 'name': 'Politics 4'},

        {'id': 'religion1', 'category_id': 'religion-category', 'name': 'Religion 1'},
        {'id': 'religion2', 'category_id': 'religion-category', 'name': 'Religion 2'},
        {'id': 'religion3', 'category_id': 'religion-category', 'name': 'Religion 3'},

        {'id': 'pop', 'category_id': 'music-category', 'name': 'Pop'},
        {'id': 'rock', 'category_id': 'music-category', 'name': 'Rock'},
        {'id': 'country', 'category_id': 'music-category', 'name': 'Country'},
    ]

def random_event(start, end, group_id):
    event = {
        'id': uuid.uuid4().hex,
        'start': start,
        'end': end,
        'title': 'This is some event on {}'.format(start),
        'description': 'Longer text description of the event',
        'group_id': group_id,
    }

    return event


def generate_events():
    for group in generate_groups():
        current_timestamp = datetime.datetime.utcnow().timestamp()
        six_months_ahead = current_timestamp + (60 * 60 * 24 * 31 * 6)

        while current_timestamp < six_months_ahead:
            start = datetime.datetime.utcfromtimestamp(current_timestamp).isoformat() + 'Z'
            end = datetime.datetime.utcfromtimestamp(current_timestamp).isoformat() + 'Z'

            event = random_event(start, end, group['id'])
            yield event

            # Create next event 1-5 days ahead
            current_timestamp += random.randint(60 * 60 * 24, 60 * 60 * 24 * 5)
