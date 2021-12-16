#
# test.py - file to test server.py
#
# this file uses pytest. all test functions need to begin with `test_`
#
from time import sleep
import pytest
import server

test_ship_id = 1


def test_example_parameters():
    rsp = server.app.test_client().get('/example/parameters/1/shipin')
    assert rsp.json == {"param1": 1, "param2": "shipin"}


def test_example_posting_json():
    test_object = {"this": "is", "my": ["test", "object"]}
    rsp = server.app.test_client().post('/example/posting-json', json=test_object)
    assert rsp.json == {"obj": test_object}


def test_example_post_and_get_ship():
    global test_ship_id
    test_object = {"name": "British Captain", "type": "Oil/Chemical Tanker"}
    rsp = server.app.test_client().post('/ships', json=test_object)
    assert "id" in rsp.json
    test_ship_id = rsp.json['id']
    rsp = server.app.test_client().get(f'/ship/{test_ship_id}')
    assert rsp.json == {"status": 1, "id": test_ship_id, "name": "British Captain", "type": "Oil/Chemical Tanker"}


def test_log_ship_and_view_ships_by_location():
    test_object = {"lat": 12, "lon": 1.2, "id": test_ship_id}
    for i in range(0, 2):
        sleep(1)
        # log ship location
        rsp = server.app.test_client().post(f'/ships/location', json=test_object)
        assert rsp.json.get('status') == 1
    del test_object["id"]
    # get ships that are in detailed location
    rsp = server.app.test_client().get(f'/location?lat={test_object["lat"]}&lon={test_object["lon"]}')
    assert rsp.json.get('status') == 1
    ids = [ship['id'] for ship in rsp.json.get('ships')]
    assert test_ship_id in ids


def test_view_ship_location():
    rsp = server.app.test_client().get(f'/ship/{test_ship_id}/location')
    assert rsp.json.get('status') == 1 and 'locations' in rsp.json
    test_location = rsp.json.get('locations')[0]
    rsp = server.app.test_client().get(f'/ship/{test_ship_id}/location?df={test_location["datetime"]}'
                                       f'&dt={test_location["datetime"]}')
    assert rsp.json.get('status') == 1
    assert 'locations' in rsp.json
    assert len(rsp.json.get('locations')) == 1
