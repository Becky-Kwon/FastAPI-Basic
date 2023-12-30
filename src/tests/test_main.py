from fastapi.testclient import TestClient
from database.orm import ToDo
from main import app

# fixture 사용하면 정의 할 필요 없음
# client = TestClient(app= app)

def test_health_check(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"ping" : "pong"}

def test_get_todos(client):
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == {
        "todos" :[
            {"id": 1, "is_done": True, "contents": "FastAPI Section 0"},
            {"id": 2, "is_done": True, "contents": "FastAPI Section 1"},
            {"id": 3, "is_done": True, "contents": "FastAPI Section 2"},
            ]
        }
    
    # order = DESC
    response = client.get("/todos?order=DESC")
    assert response.status_code == 200
    assert response.json() == {
        "todos" :[
            {"id": 3, "is_done": True, "contents": "FastAPI Section 2"},
            {"id": 2, "is_done": True, "contents": "FastAPI Section 1"},
            {"id": 1, "is_done": True, "contents": "FastAPI Section 0"},
            ]
        }

# PyTest Mocking 사용해보기
# Unit Test 를 작성할 때 외부에 의존하는 부분을 임의의 가짜로 대체하는 기법이 자주 사용되는데 이를 모킹 Mocking 이라고 한다.
# 모킹 Mocking 은 외부 서비스에 의존하지 않고 독립적으로 실행이 가능한 Unit Test 를 작성하기 위해 사용되는 테스팅 기법 
# pip install pytest-mock   


def test_get_todos_mocking(client, mocker):
    #order = ASC
    mocker.patch("main.get_todos", return_value = [
        ToDo(id=1, contents="FastAPI Section 0", is_done = True),
        ToDo(id=2, contents="FastAPI Section 1", is_done = False),
    ])
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == {
        "todos" :[
            {"id": 1, "is_done": True, "contents": "FastAPI Section 0"},
            {"id": 2, "is_done": False, "contents": "FastAPI Section 1"},
            ]
        }
    
    # order = DESC
    response = client.get("/todos?order=DESC")
    assert response.status_code == 200
    assert response.json() == {
        "todos" :[
            {"id": 2, "is_done": False, "contents": "FastAPI Section 1"},
            {"id": 1, "is_done": True, "contents": "FastAPI Section 0"},
            ]
        }


# PyTest Fixture : 
    # client = TestClient(app= app)의 client 객체가 여러 곳에서 사용 가능하게,
    #  client객체를 fixture로 바꿔보기
    # 1. tests 폴더 안에 conftest.py 만들기


# 테스트 코드 - GET 단일 조회 API
def test_get_todo(client, mocker):
    # 200
    mocker.patch(
        "main.get_todo_by_todo_id", 
        return_value = ToDo(id=1, contents="FastAPI Section 0", is_done = True)
        )
    response = client.get("/todos/1")
    assert response.status_code == 200
    assert response.json() ==  {"id": 1, "is_done": True, "contents": "FastAPI Section 0"}

    # 404
    mocker.patch(
        "main.get_todo_by_todo_id", 
        return_value = None
        )
    response = client.get("/todos/1")
    assert response.status_code == 404
    assert response.json() ==  {'detail' : "Todo Not Found"}

# 테스트 코드 - POST API
def test_create_todo(client, mocker):
    create_spy  = mocker.spy(ToDo, "create")   # main의 ToDo.create 부분을 spy함
    mocker.patch(
        "main.create_todo", 
        return_value = ToDo(id=1, contents="todo", is_done = True)
        )
    body = {
        "contents" : "test",
        "is_done" : False
    }
    # 말이안되게도 test결과 pass 다... mocking에 걸려서 그렀다... -> spy 사용하기
    response = client.post("/todos", json = body)
    assert create_spy.spy_return.id is None
    assert create_spy.spy_return.contents == "test"
    assert create_spy.spy_return.is_done is False
    
    assert response.status_code == 201
    assert response.json() ==  {"id": 1, "is_done": True, "contents": "todo"}






## 만약에 pytest를 함수별로 보고 싶다면,
# pytest tests/test_main.py::test_get_todo 이런식으로 실행하면됨