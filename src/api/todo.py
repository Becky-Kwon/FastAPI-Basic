# API 분리 -  Router를 사용해 main.py에 연결
from typing import List

from fastapi import FastAPI, Body, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from database.connection import get_db
from database.repository import get_todos, get_todo_by_todo_id, create_todo, update_todo, delete_todo
from database.orm import ToDo

from schema.request import CreateToDoRequest
from schema.response import ToDoListSchema, ToDoSchema

# API router객체 생성,@router -> router로 바꿈
# main.py 코드도 router를 연결해주고, pytest 코드도 다 바꿔줘야함
router = APIRouter()


# default 200 인데, 명시적으로 적어주는게 좋음
@router.get("/todos", status_code= 200) # resource는 복수형
# query parameter 사용해보기 -> order
# order값이 없어도 동작 할 수 있게 default로 None 하기

# GET API 전체조회
def get_todos_handler(
        order : str | None = None,
        session: Session = Depends(get_db)
    )  -> ToDoListSchema :
    # ret = list(todo_data.values())
    # if order and order == "DESC" :
    #     return ret[::-1]
    # return ret
    # DB사용해서 조회해보기
    todos: List[ToDo] = get_todos(session = session)
    if order and order == "DESC" :
        return ToDoListSchema(
        todos = [ToDoSchema.from_orm(todo) for todo in todos[::-1]]
        )
    return ToDoListSchema(
        todos = [ToDoSchema.from_orm(todo) for todo in todos]
    )


# GET API 단일 조회  {} : sub path
@router.get("/todos/{todo_id}" , status_code= 200)
def get_todo_handler(
    todo_id : int,
    session: Session = Depends(get_db),
    ) -> ToDoSchema:
    todo : ToDo | None = get_todo_by_todo_id(session= session, todo_id=todo_id)
    if todo:
        return ToDoSchema.from_orm(todo)
    raise HTTPException(status_code=404, detail="Todo Not Found")


# uvicorn main@router --reload -> --reload 옵션 : 코드 변화가 감지되면 자동으로 fastapi를 재시작 함

# POST API 생성 -> request body 필요 -> pydantic 사용
# Refactoring 해줌
# CreateToDoRequest 모듈 Refactoring으로 request.py로 넘어감

# pydantic으로 받은 데이터를 orm으로 생성해줘야함
@router.post("/todos", status_code=201)  # 생성 상태코드는 201
def create_todo_handler(
    request : CreateToDoRequest,
    session: Session = Depends(get_db)
) -> ToDoSchema:
    todo : ToDo = ToDo.create(request=request)  # id 없음
    todo : ToDo = create_todo(session=session, todo = todo)  # DB에 넣어졌다가 다시 나와서(refresh) id 생성되어 있음
    return ToDoSchema.from_orm(todo)
# DB 에 이렇게 데이터 넣어주면, server를 내렸다가 올려도 데이터가 유지됨.


# PATCH API - 수정
@router.patch("/todos/{todo_id}", status_code=200 )
def update_todo_handler(
    todo_id : int,
    is_done : bool = Body(..., embed = True),  #  ... 이니깐 required,
    # fast api는 리퀘스트 바디가 하나밖에 없으면 키값을 생략하고 리퀘스트 바디 안의 데이터만 해석하도록 되어있다.
    # ->  리퀘스트 바디의 key값을 넣어주고 싶다면 embed = True
    session: Session = Depends(get_db)
):
    todo : ToDo | None = get_todo_by_todo_id(session= session, todo_id=todo_id)
    # orm.py에 done, undone 메소드로 is_done 인스턴스 가져와서 변경
    if todo:
        # update
        todo.done() if is_done else todo.undone() # 여기서 DB까지 수정된건 아님 -> repository에 함수 추가
        todo : ToDo = update_todo(session=session, todo = todo) 
        return ToDoSchema.from_orm(todo)
    raise HTTPException(status_code=404, detail="Todo Not Found")


# DB에 저장해두는 게 아닐경우, 
# post, patch 해도 서버가 계속 꺼졌다 켜지면서 데이터 저장되지 않음

# DELETE API - 삭제
@router.delete("/todos/{todo_id}", status_code= 204)  #204는 응답되는 body가 없음
def delete_todo_handler(
    todo_id : int,
    session: Session = Depends(get_db)
):
    todo : ToDo | None = get_todo_by_todo_id(session= session, todo_id=todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo Not Found")
    # delete
    delete_todo(session=session, todo_id=todo_id)
# 정상으로 삭제되면 204 코드 뜸
 


###### 떠오른 질문
# 1. reload 하다가 ctrl + c가 눌러지지 않는다.. 무한 실행....해결 방법
#
#
#

# pip install sqlalchemy
# pip install pymysql <- python 과 mysql 연동
# pip install cryptography <- pymysql 사용시 인증이나 암호  관련 처리

