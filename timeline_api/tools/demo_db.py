
import datetime
import random
import uuid

def generate_categories():
    return [
        {'id': 'sport-category', 'name': 'Sport'},
        {'id': 'politics-category', 'name': 'Politics'},
        {'id': 'religion-category', 'name': 'Religion'},
        {'id': 'music-category', 'name': 'Music'},
        {'id': 'local-category', 'name': 'Local'},
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

        {'id': 'local1', 'category_id': 'local-category', 'name': 'Local 1'},
        {'id': 'local2', 'category_id': 'local-category', 'name': 'Local 2'},
        {'id': 'local3', 'category_id': 'local-category', 'name': 'Local 3'},
        {'id': 'local4', 'category_id': 'local-category', 'name': 'Local 4'},
    ]

def random_event(start, end, group_id):

    description = """
### Lorem ipsum
Lorem ipsum dolor sit amet, __consectetur adipiscing elit__. Duis diam sapien, tempus sed ultrices eu, **hendrerit quis justo**. Cras at quam eleifend, rhoncus nunc at, viverra elit. Vivamus consectetur eu magna quis laoreet. Morbi mauris dolor, blandit at lacus a, mattis dapibus arcu. Cras vitae auctor eros. Cras vestibulum lacinia lacus, at condimentum nisl scelerisque vel. Pellentesque fermentum dolor volutpat, ullamcorper mi a, iaculis nisl. In in orci ac odio venenatis faucibus. Donec et finibus erat. Donec fringilla velit id tellus blandit aliquam. Integer nec laoreet nisl. Suspendisse nec gravida diam. Donec euismod facilisis massa in fermentum. Pellentesque eleifend nisl sed tristique condimentum.

### Auctor felis
Nulla lobortis auctor felis, at feugiat justo molestie eget. Praesent blandit ligula eros, ac euismod ex placerat et. Praesent risus libero, pharetra vitae purus vitae, hendrerit imperdiet nibh. Maecenas eget euismod ex. Maecenas sit amet ante sit amet tortor suscipit luctus.
Praesent id erat dui:
- Mauris 
- tristique
- pellentesque

### Vitae semper
Nunc laoreet eu magna vitae semper. Vivamus ac luctus lorem, pretium sollicitudin justo. Sed varius lobortis fermentum. Aliquam ut sapien eu nisi vehicula sagittis. Cras dignissim facilisis semper. Integer tristique at odio eget sodales. Phasellus luctus magna dolor, vitae iaculis libero tempus a. Vestibulum imperdiet metus quis purus dignissim mattis.
    """

    event = {
        'id': uuid.uuid4().hex,
        'start': start,
        'end': end,
        'title': 'This is an event {}'.format(random.randint(0, 1000)),
        'description': description,
        'group_id': group_id,
    }

    return event


def generate_events():
    for group in generate_groups():
        current_timestamp = datetime.datetime.utcnow().timestamp()
        six_months_ahead = current_timestamp + (60 * 60 * 24 * 31 * 6)

        # Create first event 1-3 days ahead
        current_timestamp += random.randint(60 * 60 * 24, 60 * 60 * 24 * 3)

        while current_timestamp < six_months_ahead:
            start = datetime.datetime.utcfromtimestamp(current_timestamp).isoformat() + 'Z'
            end = datetime.datetime.utcfromtimestamp(current_timestamp).isoformat() + 'Z'

            event = random_event(start, end, group['id'])
            yield event

            # Create next event 1-5 days ahead
            current_timestamp += random.randint(60 * 60 * 24, 60 * 60 * 24 * 5)
