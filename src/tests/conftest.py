import pytest
from fastapi.testclient import TestClient
from main import app


# 아래의 fixture 데코레이터 추가해주면, 
# pytest가 client를 fixture로 인식
# tests 코드 안에서 글로벌 하게 사용 할 수 있음
@pytest.fixture
def client():
    return TestClient(app= app)



