from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from database.orm import ToDo, User
from database.connection import get_db
from fastapi import Depends
from typing import List

# repository 의 모든 def를 묶어서 class로 만듬 (래포지토리 패턴 실습) -> main 가서도 바꿔야함
class ToDoRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    # GET 전체 조회 API (DB통해서)
    def get_todos(self) -> List[ToDo]:
        return list(self.session.scalars(select(ToDo)))


    # 단일 todo 조회 API (DB통해서)
    def get_todo_by_todo_id(self, todo_id: int) -> ToDo | None:
        return self.session.scalar(select(ToDo).where(ToDo.id == todo_id)) 

    # DB에 데이터 넣기 (create todo)
    # ToDo는 orm 객체
    def create_todo(self, todo: ToDo) -> ToDo:
        self.session.add(instance=todo) # session 객체에 orm객체 쌓임
        self.session.commit() # DB에 save됨, id 값이 할당됨
        self.session.refresh(instance=todo) # DB에서 다시 한번 데이터를 읽어옴 -> todo id 값이 반영되어 있음
        return todo


    # todo의 is_done에 변경될 경우, DB에서 수정 반영해줌
    # create_todo과 코드가 같지만 따로 관리해주는게 좋아서 따로 하나 만듬
    def update_todo(self, todo: ToDo) -> ToDo:
        self.session.add(instance=todo) # session 객체에 orm객체 쌓임
        self.session.commit() # DB에 save됨, id 값이 할당됨
        self.session.refresh(instance=todo) # DB에서 다시 한번 데이터를 읽어옴 -> todo id 값이 반영되어 있음
        return todo

    def delete_todo(self, todo_id: int) -> None:
        self.session.execute(delete(ToDo).where(ToDo.id == todo_id))
        self.session.commit()



class UserRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def save_user(self, user: User) -> User:
        self.session.add(instance=user) # session 객체에 orm객체 쌓임
        self.session.commit() # DB save
        self.session.refresh(instance=user) # DB에서 다시 한번 데이터를 읽어옴
        return user