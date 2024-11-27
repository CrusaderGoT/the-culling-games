'''
test file for the matches router/paths
'''
from typing import Literal
from fastapi.testclient import TestClient
from app.models.player import PlayerInfo
from fastapi.encoders import jsonable_encoder as je
from pprint import pprint


player_info_keys = PlayerInfo.model_fields.keys()
'expected return keys, for the playerinfo'



def test_create_match(authenticated_admin_client: tuple[TestClient, dict], setup_match_players):
    'test function for creating a match'
    # test create match
    res = authenticated_admin_client[0].post("/match/create?part=1")
    print(setup_match_players)
    assert res.is_success == True



def test_upgrade_player(setup_match_players: list[tuple[TestClient, dict]]):
    'test for player upgrade'
    param = {
        "grade_up": 2
    }
    player_id = setup_match_players[1][1]["id"]
    print(player_id)
    res = setup_match_players[1][0].post(f"/player/upgrade/{player_id}", params=param)
    print(res.json())
    assert res.is_success == True # change later to True
    # confirm player info was returned
    assert res.json().keys() == player_info_keys