'''
test file for the users routers/paths
'''
from .utils_test import gen_rand_email, gen_rand_username
from fastapi.testclient import TestClient
from ..models.user import CreateUser, EditUser, UserInfo, Country
from fastapi.encoders import jsonable_encoder as je
from datetime import date


user_info_keys = UserInfo.model_fields.keys() # expected keys
'expected return keys, for the user route/ userinfo'

def test_create_user(test_client: TestClient):
    'test for the creation of a user'
    username = gen_rand_username()
    email = gen_rand_email()
    create_user_payload = CreateUser(
    username=username,
    email=email,
    country=Country("NG"),
    password="Crusader45@",
    confirm_password="Crusader45@"
    )
    response = test_client.post("/signup", json=je(create_user_payload))
    # check status is created
    assert response.status_code == 201
    # check returned keys are the expected keys
    res_keys = response.json().keys() # response keys
    assert res_keys == user_info_keys
    # check database calculated fields was made
    assert response.json()["id"] is not None and type(response.json()["id"]) is int
    assert response.json()["created"] == str(date.today())
    # check userpayload values match the response user
    for k in create_user_payload.model_dump().keys():
        if k in res_keys:
            assert response.json()[k] == create_user_payload.model_dump()[k]


def test_current_user(authenticated_test_client: tuple[TestClient, dict]):
    'test get the current user'
    response = authenticated_test_client[0].get("/users/me")
    # check status is successful
    assert response.is_success == True
    # check returned keys are the expected keys
    res_keys = response.json().keys() # response keys
    assert res_keys == user_info_keys
    # check database calculated fields was made
    assert response.json()["id"] is not None and type(response.json()["id"]) is int
    assert response.json()["created"] is not None and type(response.json()["created"]) is str
    # check if response values match setup user values
    assert response.json()["username"] == authenticated_test_client[1]["username"]
    assert response.json()["email"] == authenticated_test_client[1]["email"]

def test_a_user(authenticated_test_client: tuple[TestClient, dict]):
    'test for getting a specific user'
    auth_user = authenticated_test_client[1]
    response = authenticated_test_client[0].get(f"/users/{auth_user["id"]}")
    # check status is successful
    assert response.is_success == True
    # check returned keys are the expected keys
    res_keys = response.json().keys() # response keys
    assert res_keys == user_info_keys
    # check database calculated fields was made
    assert response.json()["id"] == auth_user["id"] and type(response.json()["id"]) is int
    assert response.json()["created"] is not None and type(response.json()["created"]) is str
    # check if response values match setup user values
    assert response.json()["username"] == auth_user["username"]
    assert response.json()["email"] == auth_user["email"]

def test_edit_user(authenticated_test_client: tuple[TestClient, dict]):
    'test for edit user'
    user = authenticated_test_client[1]
    username=gen_rand_username()
    email=gen_rand_email()
    edit_user_payload = EditUser(
        username=username,
        email=email,
        country=Country("JP")
    )
    response = authenticated_test_client[0].patch(f"/users/edit/{user["id"]}", json=je(edit_user_payload))
    # check status is successful
    assert response.is_success == True
    # check returned keys are the expected keys
    res_keys = response.json().keys() # response keys
    assert res_keys == user_info_keys
    # check constant database fields is still same
    assert response.json()["id"] == user['id'] and type(response.json()["id"]) is int
    assert response.json()["created"] is not None and type(response.json()["created"]) is str
    # check edituserpayload values match the response user
    for k in edit_user_payload.model_dump().keys():
        if k in res_keys:
            assert response.json()[k] == edit_user_payload.model_dump()[k]

def test_delete_user(authenticated_test_client: tuple[TestClient, dict]):
    user = authenticated_test_client[1]
    response = authenticated_test_client[0].delete(f"/users/delete/{user["id"]}")
    # check status is successful
    assert response.is_success == True
    # check returned keys are the expected keys
    res_keys = response.json().keys() # response keys
    assert res_keys == user_info_keys
    # check database calculated fields matches
    assert response.json()["id"] == user['id'] and type(response.json()["id"]) is int
    assert response.json()["created"] is not None and type(response.json()["created"]) is str
    # check if user no longer exists in database
    deleted_response = authenticated_test_client[0].get(f"users/{user['id']}")
    # check status, should be unsuccessful
    assert deleted_response.is_client_error == True
    
