from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy.orm import sessionmaker
from app.config import settings
from sqlalchemy import create_engine
from app.database import get_db, Base
import pytest
from app.oauth2 import create_access_token
from datetime import datetime, timedelta, UTC
from jose import jwt

# added _test to the database to connect to test databse
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
# models.Base.metadata.create_all(bind=engine)
TestingSessionLocal = sessionmaker( bind=engine, autocommit=False, autoflush=False)

@pytest.fixture(scope="function")
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client(session):
    # Dependency
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    # run our code before the tests are ran
    yield TestClient(app)
    # drop the database data


@pytest.fixture
def test_user(client):
    user_data = {"email": "test@gmail.com","password": "123"}
    response = client.post("/users/", json=user_data)

    assert response.status_code == 201

    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client

@pytest.fixture
def invalid_token(test_user):
    to_encode = {"user_id": test_user['id']}.copy()

    expire = datetime.now(UTC) + timedelta(microseconds=1)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

    return encoded_jwt