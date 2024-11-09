'''
test file for the matches router/paths
'''
from typing import Literal
from fastapi.testclient import TestClient

from app.models.player import PlayerInfo


player_info_keys = PlayerInfo.model_fields.keys()
'expected return keys, for the playerinfo'

"""def test_upgrade_player(
        autheticated_commiter_client: TestClient,
        player_id: Literal[1]):
    'test for player upgrade'
    param = {
        "grade_up": 2
    }
    res = autheticated_commiter_client.post(f"/player/upgrade/{player_id}", params=param)
    assert res.is_success == False # change later to True
    # confirm player info was returned
    assert res.json().keys() == player_info_keys"""