from app import schemas
from jose import jwt
from app.config import settings
import pytest
from app.oauth2 import oauth2_scheme

def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Bonne nuit":"Dobra noc"}

def test_create_user(client):
    response = client.post("/signup",json={"email":"test3@gmail.com","password":"123"})
    new_user = schemas.UserOut(**response.json())
    assert response.status_code == 201
    assert new_user.email == "test3@gmail.com"

def test_login_user(client,user):
    response = client.post("/login",data={"username":user['email'],"password":user['password']})
    login_response = schemas.Token(**response.json())
    payload = jwt.decode(login_response.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == user["id"]
    assert login_response.token_type == "bearer"
    assert response.status_code == 200


    
@pytest.mark.parametrize("email, password, status_code",[
    ('wrongemail@gmail.com', 'password123', 403),
    ('sanjeev@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('sanjeev@gmail.com', None, 422)
])
def test_incorrect_login(client,email, password, status_code):
    response = client.post("/login",data={"username":email,"password":password})
    assert response.status_code == status_code
    if status_code == 403:
        assert response.json().get('detail') == 'Invalid Credentials'

def test_verify_invalid_token(client, invalid_token):
    response = client.post('/verify_token',headers={'Authorization':f'Bearer {invalid_token}'})
    assert response.status_code == 401

def test_verify_token(client, token):
    response = client.post('/verify_token',headers={'Authorization':f'Bearer {token}'})
    assert response.status_code == 200
