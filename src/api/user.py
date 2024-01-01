from fastapi import APIRouter, Depends,  HTTPException

from database.repository import UserRepository
from schema.request import SignUpRequest, LogInRequest
from schema.response import UserSchema, JWTResponse
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

 
@router.post("/log-in")
def user_log_in_handler(
    request: LogInRequest,
    user_repo: UserRepository = Depends(),
    user_service: UserService = Depends()
):
    # 1. request body(username, password)
    # 2. db read user
    user: User | None = user_repo.get_user_by_username(username=request.username)
    
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
    
    # 3. user.password, reques.password -> bcrypt.checkpw
    verified: bool = user_service.verify_password(
        plain_password=request.password,
        hashed_password=user.password
    )
    if not verified:
        raise HTTPException(status_code=401, detail="Not Authorized")
    
    # 4. create jwt  (pip install python-jose)
    access_token: str = user_service.create_jwt(username=user.username)
    # 5. return jwt
    return JWTResponse(access_token=access_token)

# 로그인 API확인해보고자 user table 업데이트
# >>> import bcrypt
# >>> password = "password".encode("UTF-8")
# >>> h = bcrypt.hashpw(password, salt=bcrypt.gensalt())
# >>> h.decode("UTF-8")
#'$2b$12$OimOXlUsb8OrdrPJzCi8g.wqzCQahIJLwDHzZXI6b4SvNXoh6bQ8a'
# mysql> update user set password = '$2b$12$OimOXlUsb8OrdrPJzCi8g.wqzCQahIJLwDHzZXI6b4SvNXoh6bQ8a'where id = 1;
