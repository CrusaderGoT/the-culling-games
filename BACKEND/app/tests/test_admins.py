'''
test file for the admin router/paths
'''
from fastapi.testclient import TestClient
from ..models.admin import CreatePermission, PermissionInfo
from ..models.base import ModelName, BasePermission
from fastapi.encoders import jsonable_encoder as je

perm_keys = PermissionInfo.model_fields.keys()

def test_new_permission(authenticated_admin_client: tuple[TestClient, dict]):
    'function for testing creation of new permissions'
    levels = {BasePermission.PermissionLevel.CREATE, BasePermission.PermissionLevel.DELETE}
    modelname = ModelName.match
    payload= [
        CreatePermission(model=modelname, level=levels)
    ]
    res = authenticated_admin_client[0].post("/admin/new/permission", json=je(payload))
    assert res.is_success == True

    # confirm items in dict are perms'
    for perm in res.json():
        assert perm.keys() == perm_keys

