import datetime
import pytest
from fastapi import HTTPException
from jose import jwt
from starlette import status
from app.api.auth import ALGORITHM, SECRET_KEY, get_current_user
from app.api.auth import authenticate_user, create_access_token
from app.tests.conftest import TestingSessionLocal


def test_authentication(client, test_user):
    db = TestingSessionLocal()
    user = authenticate_user(test_user.username, "testpassword", db)
    assert user is not None
    assert user.username == test_user.username


    wrong_user = authenticate_user("wrong_username", "testpassword", db)
    assert wrong_user is None


def test_create_access_token(test_user):
    test_token = create_access_token(test_user.username, test_user.id, test_user.role, datetime.timedelta(minutes=20))

    decoded_token = jwt.decode(test_token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_signature": False})

    assert decoded_token["sub"] == test_user.username
    assert decoded_token["role"] == test_user.role
    assert decoded_token["id"] == test_user.id
    assert decoded_token["exp"] == int((datetime.datetime.now(datetime.UTC) + datetime.timedelta(seconds=1200)).timestamp())


@pytest.mark.asyncio
async def test_get_current_user_valid_token(test_user):
    encode = {'sub': test_user.username, 'id': test_user.id, 'role': test_user.role}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    user = await get_current_user(token)
    assert user == {'username': test_user.username, 'id': test_user.id, 'role': test_user.role}


@pytest.mark.asyncio
async def test_get_current_user_missing_payload(test_user):
    encode = {'role': test_user.role}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token)

    assert excinfo.value.status_code == status.HTTP_404_NOT_FOUND
    assert excinfo.value.detail == 'Invalid Credentials'
