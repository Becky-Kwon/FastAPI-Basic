from fastapi import APIRouter, Depends

from database.repository import UserRepository
from schema.request import SignUpRequest
from schema.response import UserSchema
from service.user import UserService
from database.orm import User

router = APIRouter(prefix="/users")

@router.post("/sign-up", status_code=201)
def user_sign_up_handler(
    request: SignUpRequest,
    user_service: UserService = Depends(),
    user_repo: UserRepository = Depends()
    ):
    # 1. request body(username, password)
    # hashing위한 라이브러리 설치 : pip install bcrypt
    # 2. password -> hasing -> hashed_password
    # aaa -> hash -> asdfqwefj => 개발자도 비번 모르게 됨...
    hashed_password: str = user_service.hash_password(plain_password=request.password)
    
    # 3. User(username, hashed_password) -> ORM user객체 생성
    user: User = User.create(
        username=request.username,
        hashed_password=hashed_password
    )

    # 4. user -> db save
    user: User = user_repo.save_user(user=user)  # id=int

    # 5. return user(id, username)
    return UserSchema.from_orm(user)



