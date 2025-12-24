import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from starlette import status
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from app.models.auths import Users
from app.schemas.Token import Token
from app.schemas.Auth import CreateUserRequest
from argon2 import PasswordHasher
from app.db.session import db_dependency
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError

router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = '063f1d5e99a610dd89b2f42725213b1677dd44435c4a184929299be0bf7cdd36a8fc07ee21bd66c715384fb6cdaaf2c16ff9e02088bf5019ba100cbaf990fb4d'
ALGORITHM = 'HS256'
templates = Jinja2Templates(directory="app/templates")

### Pages ###
@router.get("/login-page")
def render_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/register-page")
def render_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

### Endpoints ###
def authenticate_user(username: str, password: str, db):
    user: Users = db.query(Users).filter(Users.username == username).first()
    if not user:
        return None
    if not PasswordHasher().verify(user.hashed_password, password.encode()):
        return None
    return user


def create_access_token(username: str, user_id: int, role: str, expire_delta: datetime.timedelta):
    encode = {'sub': username, 'id': user_id, 'role': role}
    expires = datetime.datetime.now(datetime.timezone.utc) + expire_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role : str = payload.get('role')
        if not username or not user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Invalid Credentials')
        return {'username': username, 'id': user_id, 'role': user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate credentials')


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=PasswordHasher().hash(create_user_request.password.encode()),
        is_active=True,
        phone_number=create_user_request.phone_number
    )
    db.add(create_user_model)
    db.commit()


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency, response: Response):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate credentials')
    token = create_access_token(user.username, user.id, user.role, datetime.timedelta(minutes=20))
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        secure=False,  # True in production
        max_age=1200
    )
    return {'access_token': token, 'token_type': 'bearer'}


@router.post("/logout")
def logout():
    response = RedirectResponse(url="/auth/login-page", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="access_token",path="/")
    return response
