from sqlalchemy import select
from sqlalchemy.orm import Session
from database.orm import ToDo
from typing import List

# GET 전체 조회 API (DB통해서)
def get_todos(session: Session) -> List[ToDo]:
    return list(session.scalars(select(ToDo)))


# 단일 todo 조회 API (DB통해서)
def get_todo_by_todo_id(session: Session, todo_id: int) -> ToDo | None:
    return session.scalar(select(ToDo).where(ToDo.id == todo_id)) 

# DB에 데이터 넣기 (create todo)
# ToDo는 orm 객체
def create_todo(session: Session, todo: ToDo):
    session.add(instance=todo) # session 객체에 orm객체 쌓임
    session.commit() # DB에 save됨, id 값이 할당됨
    session.refresh(instance=todo) # DB에서 다시 한번 데이터를 읽어옴 -> todo id 값이 반영되어 있음
    return todo



