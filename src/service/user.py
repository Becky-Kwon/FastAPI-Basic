import bcrypt
from jose import jwt
from datetime import datetime, timedelta

class UserService:
    encoding: str = "UTF-8"
    secret_key: str = "e7ad00a6a7cba5762a3cb24cbca7b6b4e8b96a33203b35dd44bd002cbb802316"
    jwt_algorithm = "HS256"

    def hash_password(self, plain_password: str) -> str:
        hashed_password: bytes = bcrypt.hashpw(
            plain_password.encode(self.encoding), 
            salt=bcrypt.gensalt())
        return hashed_password.decode(self.encoding)
    
    def verify_password(
        self, plain_password: str, hashed_password: str
    ) -> bool:
        bcrypt.checkpw(
            plain_password.encode(self.encoding),
            hashed_password.encode(self.encoding)
        )

    # 랜덤한 비밀 키 secret_key 값 만들기 (openssl rand -hex 32)

    def create_jwt(self, username: str) -> str:
        return jwt.encode(
            {
                "sub": username,  # 원래는 unique id
                "exp": datetime.now() + timedelta(days=1) #토큰은 최대 하루동안 유효
            },
            self.secret_key, 
            algorithm=self.jwt_algorithm)