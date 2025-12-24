from starlette import status
from app.models.todos import Todos
from app.tests.conftest import TestingSessionLocal


def test_read_all_authenticated(client, test_user, test_todo):
    response = client.get("/todos")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
                                {'title': 'Learn to code!',
                                'description': 'Need to learn to Code!',
                                'priority': 5,
                                'complete': True,
                                'id': 1, 'owner_id': 1},
                               ]



def test_read_one_authenticated(client, test_user, test_todo):
    response = client.get("todos/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'title': 'Learn to code!',
                                'description': 'Need to learn to Code!',
                                'priority': 5,
                                'complete': True,
                                'id': 1, 'owner_id': 1}


def test_read_one_authenticated_not_found(client, test_user, test_todo):
    response = client.get("/todos/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found.'}


def test_create_todo(client, test_user):
    request_data = {
        'title': 'New Todo!',
        'description': 'New description',
        'priority': 5,
        'complete': False,
    }
    response = client.post('/todos/todo', json=request_data)
    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')


def test_update_todo(client, test_user, test_todo):
    request_data = {
        'title': 'Change the title of the todo already saved',
        'description': 'Need to learn everyday',
        'priority': 5,
        'complete': False,
    }
    response = client.put('/todos/1', json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == request_data.get('title')


def test_update_todo_not_found(client, test_user):
    request_data = {
        'title': 'Change the title of the todo already saved',
        'description': 'Need to learn everyday',
        'priority': 5,
        'complete': False,
    }
    response = client.put('/todos/999', json=request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_todo(client, test_user, test_todo):
    response = client.delete('/todos/1')
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None


def test_delete_todo_not_found(client, test_user):
    response = client.delete('/todos/999')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found.'}