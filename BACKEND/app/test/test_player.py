'''
test file for the players routers/paths
'''

from typing import Literal
from fastapi.testclient import TestClient
from app.utils.dependencies import colony
from ..models.player import (CreatePlayer, CreateCT, 
                            CreateCTApp, PlayerInfo)
from fastapi.encoders import jsonable_encoder


player_info_keys = PlayerInfo.model_fields.keys()
'expected return keys, for the player route/ playerinfo'


def test_create_player(autheticated_test_client: TestClient,
                       user_id: Literal[1]):
    'test function for creating a player'
    c_player_payload = CreatePlayer(
        name="testplayer",
        gender=CreatePlayer.Gender("male"),
        age=25,
        role="programmer"
    )
    c_ct = CreateCT(
        name="git push",
        definition="commit on friday"
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
    new_player_payload = jsonable_encoder(player_dict)
    created_res = autheticated_test_client.post(f"/player/create/{user_id}", json=new_player_payload)
    assert created_res.is_success == True
    res_keys = created_res.json().keys()
    assert res_keys == player_info_keys