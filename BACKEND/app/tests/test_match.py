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

def test_create_match(authenticated_admin_client: tuple[TestClient, dict], match_players):
    'test function for creating a match'
    # test create match
    res = authenticated_admin_client[0].post("/match/create?part=1")
    assert res.is_success == True

def test_vote_player(authenticated_test_client: tuple[TestClient, dict], authenticated_admin_client: tuple[TestClient, dict], match_players: list[tuple[TestClient, dict]]):
    "test voting of a player, using an auth client, admin client, etc."
    def _votes():
        'votes for use in test'
        votes_payload = [
            CastVote(
                player_id=match_players[0][1]["id"], # player 1 ID
                ct_app_id=choice(
                    [app["id"] for app in match_players[0][1]["cursed_technique"]["applications"]]
                ) # random select from player 1 ct apps
            ),
            CastVote(
                player_id=match_players[1][1]["id"], # player 2 ID
                ct_app_id=choice(
                    [app["id"] for app in match_players[1][1]["cursed_technique"]["applications"]]
                ) # random select from player 2 ct apps
            ),
        ]
        return votes_payload
    votes = _votes()
    # test for a regular user
    res0 = authenticated_test_client[0].post("/match/vote/1", json=je(votes))
    assert res0.is_success == True
    # check if all votesere casted
    assert len(res0.json()["votes"]) == len(votes), "Not all votes were casted for regular user"

    # test for a admin user
    res1 = authenticated_admin_client[0].post("/match/vote/1", json=je(votes))
    assert res1.is_success == True
    # check if all votesere casted
    assert len(res0.json()["votes"]) == len(votes), "Not all votes were casted for admin user"

    # test for the users of the player
    res3 = match_players[0][0].post("/match/vote/1", json=je(votes))
    assert res3.is_success == True
    # check if all votesere casted
    assert len(res0.json()["votes"]) == len(votes), "Not all votes were casted for player 1 user"

    res4 = match_players[1][0].post("/match/vote/1", json=je(votes))
    assert res4.is_success == True
    # check if all votesere casted
    assert len(res0.json()["votes"]) == len(votes), "Not all votes were casted for player 2 user"


def test_upgrade_player(match_players: list[tuple[TestClient, dict]]):
    'test for player upgrade'
    param = {
        "grade_up": 2
    }
    player1 = match_players[0]
    res = match_players[0][0].post(f"/player/upgrade/{player1[1]["id"]}", params=param)
    assert res.is_success == True # change later to True
    
    # confirm player info was returned
    assert res.json().keys() == player_info_keys
    # confirm player was upgraded
    assert res.json()["grade"] == param["grade_up"]

def test_domain_expansion(match_players: list[tuple[TestClient, dict]]):
    'test for activating domain expansion, and it various perks'
    # activate for player 1
    player1 = match_players[0][1]
    res0 = match_players[0][0].post(f"match/activate/domain/{player1['id']}", params={"match_id": 1})
    assert res0.is_success == True, f"Couldn't activate domain for player 1: {pprint(res0.json())}"
