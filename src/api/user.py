from fastapi import APIRouter, Depends, HTTPException

from database.repository import UserRepository
from schema.request import SignUpRequest, LogInRequest, CreateOTPRequest, VerifyOTPRequest
from schema.response import UserSchema, JWTResponse
from service.user import UserService
from database.orm import User
from security import get_access_token
from cache import redis_client

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


# pip install redis
# OTP 기능 만들기

# 회원가입(username, password) / 로그인
# 이메일 알림: 회원가입 -> 이메일 인증(otp) -> 유저 이메일 저장 -> 이메일 알림


# POST / users/email/otp -> otp(key: email, value: 1234, exp: 3min)
# POST / users/email/otp/verfiy -> request(email, otp) -> user(email)

@router.post("/email/otp")
def create_otp_handler(
    request: CreateOTPRequest,
    _: str = Depends(get_access_token),   #header에 검증만하고 사용은 안하니가 _ 처리
    user_service: UserService = Depends()
):
    # 1. access_token 검증
    # 2. request body(email)
    # 3. otp create(random 4 digit)
    otp: str = user_service.create_otp()

    # 4. redis otp(email, 1234, exp=3min)
    redis_client.set(request.email, otp)
    redis_client.expire(request.email, 3 * 60)
    # 5. send otp to email
    return {"otp":otp}


@router.post("/email/otp/verify")
def verify_otp_handler(
    request: VerifyOTPRequest,
    access_token: str = Depends(get_access_token),
    user_service: UserService = Depends(),
    user_repo: UserRepository = Depends()
):
    # 1. access_token 검증
    # 2. request body(email, otp)   
    # 3. request.otp == redis.get(email)
    otp: str | None = redis_client.get(request.email)
    if not otp:
        raise HTTPException(status_code=400, detail="Bad Request")
    
    if request.otp != int(otp): 
        raise HTTPException(status_code=400, detail="Bad Request")
    # 4. user(email)
    username: str = user_service.decode_jwt(access_token=access_token)
    user: User | None = user_repo.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
    # 5.save email to user
    return UserSchema.from_orm(user)