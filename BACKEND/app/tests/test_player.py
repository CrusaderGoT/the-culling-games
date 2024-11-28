'''
test file for the players routers/paths
'''

from fastapi.testclient import TestClient

from app.tests.utils_test import create_test_player
from ..models.player import (
    PlayerInfo,
    EditPlayer, EditCTApp, BasePlayerInfo
)
from fastapi.encoders import jsonable_encoder as je


player_info_keys = PlayerInfo.model_fields.keys()
'expected return keys, for the player route/ playerinfo'

def test_create_player(authenticated_test_client: tuple[TestClient, dict]):
    '''test function for creating a player.\n
    Note the player will not be deleted, unless the test_client.delete works.\n
    This can lead to multilpe players with no user in the database'''
    created_res = create_test_player(authenticated_test_client) 
    assert created_res.is_success == True
    res_keys = created_res.json().keys()
    assert res_keys == player_info_keys

def test_my_player(authenticated_test_client: tuple[TestClient, dict]):
    "test for getting the current user's player"
    created_player = create_test_player(authenticated_test_client)
    assert created_player.is_success == True
    res = authenticated_test_client[0].get("/player/me") # get the player of the same test user/client
    assert res.is_success == True
    # confirm player info returned for the test client matches that of the created player
    assert res.json().keys() == created_player.json().keys()
    for v in res.json().values():
        assert v in created_player.json().values()

def test_a_player(authenticated_test_client: tuple[TestClient, dict]):
    'test for getting a player'
    created_player = create_test_player(authenticated_test_client)
    assert created_player.is_success == True
    res = authenticated_test_client[0].get(f"/player/{created_player.json()["id"]}")
    assert res.is_success == True
    # confirm player info was returned
    assert res.json().keys() == player_info_keys

def test_edit_player(authenticated_test_client: tuple[TestClient, dict]):
    'test for editing a player'
    created_player = create_test_player(authenticated_test_client)
    assert created_player.is_success == True
    e_player = EditPlayer(
        name="editedplayer",
        role="tired program"
    )
    e_apps = [
        EditCTApp(number=1, application="dismantle"),
        EditCTApp(number=4, application="Cleave")
    ]
    edit_payload = {
        "player": e_player,
        "cursed_technique": None,
        "applications": e_apps
    }
    res = authenticated_test_client[0].patch(f"/player/edit/{created_player.json()["id"]}", json=je(edit_payload))
    assert res.is_success == True

def test_get_players(authenticated_test_client: tuple[TestClient, dict]):
    'test for getting all existing players'
    params = {
        "offset": 0,
        "limit": 30,
        "slim": True # False to include extra infos about the player
    }
    res = authenticated_test_client[0].get("/player/all", params=params)
    assert res.is_success == True
    # confirm player info was returned
    if res.json(): # list is not empty
        for d in res.json():
            assert d.keys() == player_info_keys or d.keys() == BasePlayerInfo.model_fields.keys()
    else:
        print("No player in returned list")
        pass

# should run last to delete the player created in test_create_player
def test_delete_player(authenticated_test_client: tuple[TestClient, dict]):
    "test for deleting a user from a database"
    created_player = create_test_player(authenticated_test_client)
    # store created player data in a variable, for use to cross check deleted player
    player = created_player.json()
    assert created_player.is_success == True
    res = authenticated_test_client[0].delete(f"/player/delete/{created_player.json()["id"]}")
    assert res.is_success == True
    # confirm player info was returned
    assert res.json().keys() == player_info_keys
    # confirm the created player was the player deleted
    assert res.json()["id"] == player["id"]