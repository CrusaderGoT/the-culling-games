'''
test file for the users routers/paths
'''
from ..models.user import CreateUser, UserInfo, Country
from fastapi.encoders import jsonable_encoder as je
from datetime import date


user_payload = CreateUser(
    username="test_username",
    email="testuser@example.com",
    country=Country("NG"),
    password="Crusader45@",
    confirm_password="Crusader45@"
)
'the user data for testing user routes'

def test_create_user(test_client):
    'test for the creation of a user'
    response = test_client.post("/signup", json=je(user_payload))
    # check status is created
    assert response.status_code == 201
    # check returned keys are the expected keys
    res_keys = response.json().keys() # response keys
    user_info_keys = UserInfo.model_fields.keys() # expected keys
    assert res_keys == user_info_keys
    # check database calculated fields was made
    assert response.json()["id"] is not None and type(response.json()["id"]) is int
    assert response.json()["created"] is not None and type(response.json()["created"]) is str
    # check userpayload values match the response user
    for k in user_payload.model_dump().keys():
        if k in res_keys:
            assert response.json()[k] == user_payload.model_dump()[k]

"""def test_current_user(test_client):
    response = test_client.get("users/me")
    print(response.json())
    assert response.is_success == True"""