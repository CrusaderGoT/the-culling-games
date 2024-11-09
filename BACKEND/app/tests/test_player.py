'''
test file for the players routers/paths
'''
# upgarde player is in match test

from typing import Literal
from fastapi.testclient import TestClient
from ..models.player import (CreatePlayer, CreateCT, 
                            CreateCTApp, PlayerInfo,
                            EditPlayer, EditCTApp)
from fastapi.encoders import jsonable_encoder as je


player_info_keys = PlayerInfo.model_fields.keys()
'expected return keys, for the player route/ playerinfo'

def test_create_player(autheticated_commiter_client: TestClient,
                       user_id: Literal[1]):
    '''test function for creating a player.\n
    Note the player will not be deleted, unless the test_client.delete works.\n
    This can lead to multilpe players with no user in the database'''
    c_player_payload = CreatePlayer(
        name="testplayer",
        gender=CreatePlayer.Gender("male"),
        age=25,
        role="programmer"
    )
    c_ct = CreateCT(
        name="git push",
        definition="commit on friday, trust me bro"
    )
    c_ct_apps = [
        CreateCTApp(application="first"),
        CreateCTApp(application="second"),
        CreateCTApp(application="third"),
        CreateCTApp(application="fourth"),
        CreateCTApp(application="fifth"),
    ]
    player_dict = {"player": c_player_payload,
                   "cursed_technique": c_ct,
                   "applications": c_ct_apps}
    created_res = autheticated_commiter_client.post(f"/player/create/{user_id}", json=je(player_dict))
    assert created_res.is_success == True
    res_keys = created_res.json().keys()
    assert res_keys == player_info_keys

def test_my_player(autheticated_commiter_client: TestClient):
    "test for getting the current user's player"
    res = autheticated_commiter_client.get("/player/me")
    assert res.is_success == True
    # confirm player info was returned
    assert res.json().keys() == player_info_keys

def test_a_player(autheticated_test_client: TestClient, player_id: Literal[1]):
    'test for getting a player'
    res = autheticated_test_client.get(f"/player/{player_id}")
    assert res.is_success == True
    # confirm player info was returned
    assert res.json().keys() == player_info_keys

def test_edit_player(autheticated_commiter_client: TestClient, player_id: Literal[1]):
    'test for editing a player'
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
    res = autheticated_commiter_client.patch(f"/player/edit/{player_id}", json=je(edit_payload))
    assert res.is_success == True

def test_get_players(autheticated_test_client: TestClient):
    'test for getting a player'
    params = {
        "offset": 0,
        "limit": 10,
        "slim": False # False to include extra infos about the player
    }
    res = autheticated_test_client.get(f"/player/all/players", params=params)
    assert res.is_success == True
    # confirm player info was returned
    assert type(res.json()) == list
    if res.json(): # list is not empty
        for d in res.json():
            assert d.keys() == player_info_keys

# should run last to delete the player created in test_create_player
def test_delete_player(autheticated_commiter_client: TestClient, player_id: Literal[1]):
    "test for deleting a user from a database"
    res = autheticated_commiter_client.delete(f"/player/delete/{player_id}")
    assert res.is_success == True
    # confirm player info was returned
    assert res.json().keys() == player_info_keys