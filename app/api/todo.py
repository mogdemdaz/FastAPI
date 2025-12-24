from typing import Annotated
from fastapi import HTTPException, APIRouter, Path, Depends, Request
from starlette import status
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.models.todos import Todos
from app.schemas.Todo import TodoRequest
from app.db.session import db_dependency
from .auth import get_current_user

router = APIRouter(prefix='/todos', tags=['todos'])
user_dependency = Annotated[dict, Depends(get_current_user)]
templates = Jinja2Templates(directory="app/templates")


def redirect_to_login():
    response = RedirectResponse(url="/auth/login-page", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("access_token")
    return response


### Pages ###
@router.get("/todo-page")
async def render_todo_page(request: Request, db: db_dependency):
    try:
        user = await get_current_user(request)
    except HTTPException as e:
        return redirect_to_login()
    todos = db.query(Todos).filter(Todos.owner_id == user.get("id")).all()
    return templates.TemplateResponse("todo.html", {"request": request, "user": user, "todos": todos})


@router.get("/add-todo-page")
async def add_todo_page(request: Request, db: db_dependency):
    try:
        user = await get_current_user(request)
    except HTTPException as e:
        return redirect_to_login()
    return templates.TemplateResponse("add-todo.html", {"request": request, "user": user})


@router.get("/edit-todo-page/{todo_id}")
async def render_edit_todo_page(request: Request, todo_id: int, db: db_dependency):
    try:
        user = await get_current_user(request)
    except HTTPException as e:
        return redirect_to_login()
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    return templates.TemplateResponse("edit-todo.html", {"request": request, "user": user, "todo": todo})


### Endpoints ###
@router.get("/")
async def read_all(user: user_dependency, db: db_dependency):
    return db.query(Todos).filter(Todos.owner_id == user.get("id")).all()


@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency,
                    db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Authentication Failed")
    todo_model = (db.query(Todos).filter(Todos.id == todo_id)
                  .filter(Todos.owner_id == user.get('id')).first())
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found.")


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency,
                      todo_request: TodoRequest,
                      db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Authentication Failed")
    todo_model = Todos(**todo_request.model_dump(), owner_id=user.get('id'))
    db.add(todo_model)
    db.commit()


@router.put("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency, db: db_dependency,
                      todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Authentication Failed")
    todo_model = (db.query(Todos).filter(Todos.id == todo_id)
                  .filter(Todos.owner_id == user.get('id')).first())
    if todo_model is not None:
        todo_model.title = todo_request.title
        todo_model.description = todo_request.description
        todo_model.priority = todo_request.priority
        todo_model.complete = todo_request.complete

        db.add(todo_model)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail='Todo not found.')


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Authentication Failed")
    todo_model = (db.query(Todos).filter(Todos.id == todo_id)
                  .filter(Todos.owner_id == user.get('id')).first())
    if todo_model is not None:
        (db.query(Todos).filter(Todos.id == todo_id)
         .filter(Todos.owner_id == user.get('id')).delete())
        db.commit()
    else:
        raise HTTPException(status_code=404, detail='Todo not found.')
