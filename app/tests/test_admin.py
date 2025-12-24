from starlette import status
from app.models.todos import Todos
from app.tests.conftest import TestingSessionLocal


def test_admin_read_all_authenticated(test_user, client, test_todo):
    response = client.get('/admin/todo')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {'title': "Learn to code!",
         'description': "Need to learn to Code!",
         'priority': 5,
         'complete': True,
         'owner_id': 1,
         'id': 1}
    ]


def test_admin_delete_todo(client, test_user, test_todo):
    response = client.delete('/admin/todo/1')
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None


def test_admin_delete_todo_not_found(client, test_user):
    response = client.delete('/admin/todo/9999')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not Found'}
