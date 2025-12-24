from starlette import status
from argon2 import PasswordHasher


def test_return_user(client, test_user):
    response = client.get('/user')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == "emeka.aziagba"
    assert response.json()['email'] == "emeka.aziagba@gmail.com"
    assert response.json()['first_name'] == "Emeka"
    assert response.json()['last_name'] == "Aziagba"
    assert response.json()['phone_number'] == "08064812342"
    assert response.json()['role'] == "admin"
    assert PasswordHasher().verify(hash=response.json()['hashed_password'], password="testpassword".encode())


def test_change_password_success(client, test_user):
    response = client.put('/user/password', json={"password": "testpassword",
                                                  "new_password": "newpassword",
                                                  "confirm_password": "newpassword"})
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_wrong_current_password(client, test_user):
    response = client.put('/user/password', json={"password": "wrongpassword",
                                                  "new_password": "newpassword",
                                                  "confirm_password": "newpassword"})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Wrong password'}


def test_change_password_wrong_confirmation_password(client, test_user):
    response = client.put('/user/password', json={"password": "testpassword",
                                                  "new_password": "newpassword",
                                                  "confirm_password": "wrongpassword"})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Password does not match'}


def test_change_phone_number(client, test_user):
    response = client.put('/user/08164737913')
    assert response.status_code == status.HTTP_204_NO_CONTENT