'''
test file for the matches router/paths
'''
from fastapi.testclient import TestClient
from app.models.player import PlayerInfo
from fastapi.encoders import jsonable_encoder as je
from ..models.match import CastVote
from random import choice
from pprint import pprint


player_info_keys = PlayerInfo.model_fields.keys()
'expected return keys, for the playerinfo'

def test_create_match(authenticated_admin_client: tuple[TestClient, dict], match_players: list[tuple[TestClient, dict]]):
    'test function for creating a match'
    # test create match
    res = authenticated_admin_client[0].post("/match/create?part=1")
    assert res.is_success == True

def test_vote_player(authenticated_test_client: tuple[TestClient, dict], authenticated_admin_client: tuple[TestClient, dict], match_players: list[tuple[TestClient, dict]]):
    "test voting of a player, using an auth client, admin client, etc."
    def votes():
        votes_payload = [
            CastVote(
                player_id=match_players[0][1]["id"], # player 1 ID
                ct_app_id=choice(
                    [app["id"] for app in match_players[0][1]["cursed_technique"]["applications"]]
                ) # random select from player 1 ct apps
            ),
        ]
        return votes_payload


    # test for a regular user
    res = authenticated_test_client[0].post("/match/vote/1", json=je(votes()))
    assert res.is_success == True
    # test for a regular user
    res1 = authenticated_test_client[0].post("/match/vote/1", json=je(votes()))
    assert res1.is_success == True


def test_upgrade_player(match_players: list[tuple[TestClient, dict]]):
    'test for player upgrade'
    param = {
        "grade_up": 2
    }
    player1 = match_players[0]
    res = match_players[0][0].post(f"/player/upgrade/{player1[1]["id"]}", params=param)
    print(res.json())
    assert res.is_success == True # change later to True
    
    # confirm player info was returned
    assert res.json().keys() == player_info_keys