# pip install fastapi  -> Uvicorn ASGI Server 를 사용
# ASGI (Asynchronous Server Gateway Interface)
# : 비동기 web server를 의미함 (DB나 API 연동 과정에서 발생하는 대기 시간을 낭비하지 않고, CPU가 다른 작업을 할 수 있도록 하는 방식)
# : async / await 구문을 사용
# pip install uvicorn  -> 4(매우 가벼운) ASGI 서버
# (fastapi framework만으로는 웹 개발을 할 수 없고, ASGI와 호환되는 웹 서버가 필요함)
# pip install pytest
# pip install httpx
# 

from fastapi import FastAPI, Body, HTTPException, Depends
from pydantic import BaseModel
from database.connection import get_db
from sqlalchemy.orm import Session

from database.repository import get_todos
from database.orm import ToDo
from typing import List

app = FastAPI()

@app.get("/")  # root path로 get 요청

# 단순히 return 해줌
def health_check_handler():
    return {"ping" : "pong"}

# http://127.0.0.1:8000/docs => swaggerUI (docs 문서) 생성된거 확인 가능
# 웹 서버 실행 후 코드를 변경하면, 웹 서버를 재시작 해야 변경사항이 SwaggerUI에 반영됩니다.
# FastAPI 서버 종료 방법: Ctrl + C


# default 200 인데, 명시적으로 적어주는게 좋음
@app.get("/todos", status_code= 200) # resource는 복수형
# query parameter 사용해보기 -> order
# order값이 없어도 동작 할 수 있게 default로 None 하기

# GET API 전체조회
def get_todos_handler(
        order : str | None = None,
        session: Session = Depends(get_db)
    ) :
    # ret = list(todo_data.values())
    # if order and order == "DESC" :
    #     return ret[::-1]
    # return ret
    # DB사용해서 조회해보기
    todos: List[ToDo] = get_todos(session = session)
    if order and order == "DESC" :
        return todos[::-1]
    return todos

# GET API 단일 조회  {} : sub path
@app.get("/todos/{todo_id}" , status_code= 200)
def get_todo_handler(todo_id : int):
    todo = todo_data.get(todo_id)
    if todo:
        return todo
    raise HTTPException(status_code=404, detail="Todo Not Found")


# uvicorn main:app --reload -> --reload 옵션 : 코드 변화가 감지되면 자동으로 fastapi를 재시작 함

# POST API 생성 -> request body 필요 -> pydantic 사용
class CreateToDoRequest(BaseModel):
    id : int
    contents : str
    is_done : bool

@app.post("/todos", status_code=201)  # 생성 상태코드는 201
def create_todo_handler(request : CreateToDoRequest):
    todo_data[request.id] = request.dict()
    return todo_data[request.id]

# PATCH API - 수정
@app.patch("/todos/{todo_id}", status_code=200 )
def update_todo_handler(
        todo_id : int,
        is_done : bool = Body(..., embed = True)  #  ... 이니깐 required,
        # fast api는 리퀘스트 바디가 하나밖에 없으면 키값을 생략하고 리퀘스트 바디 안의 데이터만 해석하도록 되어있다.
        # ->  리퀘스트 바디의 key값을 넣어주고 싶다면 embed = True
):
    # is_done만 수정하는 api 만듬 -> Body 사용
    todo = todo_data.get(todo_id)
    if todo:
        todo['is_done'] = is_done
        return todo
    raise HTTPException(status_code=404, detail="Todo Not Found")

# DB에 저장해두는 게 아니기에 post, patch 해도 서버가 계속 꺼졌다 켜지면서 데이터 저장되지 않음

# DELETE API - 삭제
@app.delete("/todos/{todo_id}", status_code= 204)  #204는 응답되는 body가 없음
def delete_todo_handler(todo_id : int):
    todo = todo_data.pop(todo_id, None) # key error 방지하고자 None
    if todo:
        return  #response body 비어져 있는것임
    # return todo_data
    raise HTTPException(status_code=404, detail="Todo Not Found")


###### 떠오른 질문
# 1. reload 하다가 ctrl + c가 눌러지지 않는다.. 무한 실행....해결 방법
#
#
#

# pip install sqlalchemy
# pip install pymysql <- python 과 mysql 연동
# pip install cryptography <- pymysql 사용시 인증이나 암호  관련 처리

