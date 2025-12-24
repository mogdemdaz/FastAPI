import pytest
from argon2 import PasswordHasher
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.base import Base
from app.db.session import get_db
from app.api.auth import get_current_user
from app.models.todos import Todos
from app.models.auths import Users

TEST_DATABASE_URL = "postgresql+psycopg://postgres:00000@localhost:5432/Test_Todo"

engine = create_engine(TEST_DATABASE_URL, future=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture
def client():
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    def override_get_current_user():
        return {'username': 'emeka.aziagba', 'id': 1, 'role': 'admin'}

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user

    yield TestClient(app)

@pytest.fixture()
def test_todo():
    todo = Todos(
        title="Learn to code!",
        description="Need to learn to Code!",
        priority=5,
        complete=True,
        owner_id=1
    )

    with engine.begin() as con:
        con.execute(text("DELETE FROM todos;"))
        con.execute(text("ALTER SEQUENCE todos_id_seq RESTART WITH 1;"))


    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo

    with engine.begin() as con:
        con.execute(text("DELETE FROM todos;"))
        con.execute(text("ALTER SEQUENCE todos_id_seq RESTART WITH 1;"))


@pytest.fixture
def test_user():
    user = Users(
        username="emeka.aziagba",
        email="emeka.aziagba@gmail.com",
        first_name="Emeka",
        last_name="Aziagba",
        phone_number="08064812342",
        hashed_password=PasswordHasher().hash("testpassword".encode()),
        role="admin"
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user

    with engine.begin() as con:
        con.execute(text("DELETE FROM Users;"))
        con.execute(text("ALTER SEQUENCE users_id_seq RESTART WITH 1;"))

