from fastapi.testclient import TestClient
from database.orm import ToDo
from main import app

client = TestClient(app= app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"ping" : "pong"}

def test_get_todos():
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == [
            {"id": 1, "is_done": True, "contents": "FastAPI Section 0"},
            {"id": 2, "is_done": True, "contents": "FastAPI Section 1"},
            {"id": 3, "is_done": False, "contents": "FastAPI Section 2"},
            ]
    
    # order = DESC
    response = client.get("/todos?order=DESC")
    assert response.status_code == 200
    assert response.json() == [
            {"id": 3, "is_done": False, "contents": "FastAPI Section 2"},
            {"id": 2, "is_done": True, "contents": "FastAPI Section 1"},
            {"id": 1, "is_done": True, "contents": "FastAPI Section 0"},
            ]

# PyTest Mocking 사용해보기
# Unit Test 를 작성할 때 외부에 의존하는 부분을 임의의 가짜로 대체하는 기법이 자주 사용되는데 이를 모킹 Mocking 이라고 한다.
# 모킹 Mocking 은 외부 서비스에 의존하지 않고 독립적으로 실행이 가능한 Unit Test 를 작성하기 위해 사용되는 테스팅 기법 
# pip install pytest-mock   


def test_get_todos_mocking(mocker):
    #order = ASC
    mocker.patch("main.get_todos", return_value = [
        ToDo(id=1, contents="FastAPI Section 0", is_done = True),
        ToDo(id=2, contents="FastAPI Section 1", is_done = False),
    ])
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == [
            {"id": 1, "is_done": True, "contents": "FastAPI Section 0"},
            {"id": 2, "is_done": False, "contents": "FastAPI Section 1"},
            ]
    
    # order = DESC
    response = client.get("/todos?order=DESC")
    assert response.status_code == 200
    assert response.json() == [
            {"id": 2, "is_done": False, "contents": "FastAPI Section 1"},
            {"id": 1, "is_done": True, "contents": "FastAPI Section 0"},
            ]


# PyTest Fixture : 
    # client = TestClient(app= app)의 client 객체가 여러 곳에서 사용 가능하게,
    #  client객체를 fixture로 바꿔보기
    # 1. tests 폴더 안에 conftest.py 만들기

