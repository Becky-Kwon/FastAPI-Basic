from database.orm import ToDo, User
from database.repository import ToDoRepository, UserRepository
from service.user import UserService

# fixture 사용하면 정의 할 필요 없음
# client = TestClient(app= app)

# PyTest Mocking 사용해보기
# Unit Test 를 작성할 때 외부에 의존하는 부분을 임의의 가짜로 대체하는 기법이 자주 사용되는데 이를 모킹 Mocking 이라고 한다.
# 모킹 Mocking 은 외부 서비스에 의존하지 않고 독립적으로 실행이 가능한 Unit Test 를 작성하기 위해 사용되는 테스팅 기법 
# pip install pytest-mock   

def test_get_todos(client, mocker):
    access_token: str = UserService().create_jwt(username="test")
    headers = {"Authorization": f"Bearer {access_token}"}

    user = User(id=1, username="test", password="hashed")
    user.todos = [
        ToDo(id=1, contents="FastAPI Section 0", is_done=True),
        ToDo(id=2, contents="FastAPI Section 1", is_done=False),
    ]

    mocker.patch.object(
        UserRepository, "get_user_by_username", return_value=user
    )

    # order=ASC
    response = client.get("/todos", headers=headers)
    assert response.status_code == 200
    assert response.json() == {
        "todos": [
            {"id": 1, "contents": "FastAPI Section 0", "is_done": True},
            {"id": 2, "contents": "FastAPI Section 1", "is_done": False},
        ]
    }

    # order=DESC
    response = client.get("/todos?order=DESC", headers=headers)
    assert response.status_code == 200
    assert response.json() == {
        "todos": [
            {"id": 2, "contents": "FastAPI Section 1", "is_done": False},
            {"id": 1, "contents": "FastAPI Section 0", "is_done": True},
        ]
    }

# PyTest Fixture : 
    # client = TestClient(app= app)의 client 객체가 여러 곳에서 사용 가능하게,
    #  client객체를 fixture로 바꿔보기
    # 1. tests 폴더 안에 conftest.py 만들기


# 테스트 코드 - GET 단일 조회 API
def test_get_todo(client, mocker):
    # 200
    mocker.patch.object(
        ToDoRepository,
        "get_todo_by_todo_id", 
        return_value = ToDo(id=1, contents="todo", is_done = True)
        )
    response = client.get("/todos/1")
    assert response.status_code == 200
    assert response.json() ==  {"id": 1, "is_done": True, "contents": "todo"}

    # 404
    mocker.patch.object(
        ToDoRepository,
        "get_todo_by_todo_id", 
        return_value = None
        )
    response = client.get("/todos/1")
    assert response.status_code == 404
    assert response.json() ==  {'detail' : "Todo Not Found"}

# 테스트 코드 - POST API
def test_create_todo(client, mocker):
    create_spy  = mocker.spy(ToDo, "create")   #"api.todo의 ToDo.create 부분을 spy함
    mocker.patch.object(
        ToDoRepository,
        "create_todo", 
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


# 테스트 코드 - PATCH API (Update API)
def test_update_todo(client, mocker):
    # 200
    mocker.patch.object(
        ToDoRepository,
        "get_todo_by_todo_id", 
        return_value = ToDo(id=1, contents="todo", is_done = True)
        )
    
    undone = mocker.patch.object(ToDo, "undone")
    mocker.patch.object(
        ToDoRepository,
        "update_todo", 
        return_value = ToDo(id=1, contents="todo", is_done = False)
        )

    response = client.patch("/todos/1", json={"is_done": False})

    undone.assert_called_once_with()

    assert response.status_code == 200
    assert response.json() ==  {"id": 1, "is_done": False, "contents": "todo"}

    # 404
    mocker.patch.object(
        ToDoRepository,
        "get_todo_by_todo_id", 
        return_value = None
        )
    response = client.patch("/todos/1", json={'is_done': True})
    assert response.status_code == 404
    assert response.json() ==  {'detail' : "Todo Not Found"}
 

# 테스트 코드 - DELETE API
def test_delete_todo(client, mocker):
    # 204
    mocker.patch.object(
        ToDoRepository,
        "get_todo_by_todo_id", 
        return_value = ToDo(id=1, contents="todo", is_done = True)
        )
    mocker.patch.object(ToDoRepository,"delete_todo", return_value = None)

    response = client.delete("/todos/1")
    assert response.status_code == 204

    # 404
    mocker.patch.object(
        ToDoRepository,
        "get_todo_by_todo_id", 
        return_value = None
        )
    response = client.get("/todos/1")
    assert response.status_code == 404
    assert response.json() ==  {'detail' : "Todo Not Found"}




## 만약에 pytest를 함수별로 보고 싶다면,
# pytest tests/test"main.py::test_get_todo 이런식으로 실행하면됨