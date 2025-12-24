from typing import Annotated

from argon2.exceptions import VerifyMismatchError
from fastapi import HTTPException, APIRouter, Path, Depends
from starlette import status
from app.models.todos import Todos
from app.models.auths import Users
from app.schemas.UserAuth import UserAuth
from app.schemas.Todo import TodoRequest
from app.db.session import db_dependency
from .auth import get_current_user
from argon2 import PasswordHasher

router = APIRouter(prefix='/user', tags=['user'])
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return db.query(Users).filter(Users.id == user.get('id')).first()


@router.put('/password', status_code=status.HTTP_204_NO_CONTENT)
async def update_password(user: user_dependency, db: db_dependency,
                          user_verification: UserAuth):
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    user_model:Users = db.query(Users).filter(Users.id == user.get('id')).first()
    try:
        PasswordHasher().verify(user_model.hashed_password, user_verification.password.encode())
    except VerifyMismatchError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Wrong password')
    if user_verification.new_password != user_verification.confirm_password:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Password does not match')
    user_model.hashed_password = PasswordHasher().hash(user_verification.new_password.encode())
    db.add(user_model)
    db.commit()


@router.put('/{phone_number}', status_code=status.HTTP_204_NO_CONTENT)
async def update_phone_number(user: user_dependency, db: db_dependency, phone_number: str):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed!')
    user_model:Users = db.query(Users).filter(Users.id == user.get('id')).first()
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()