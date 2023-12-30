# HTTP Response 처리
# 왜 이렇게 Response를 분리하고 한 번 더 정의해서 쓰나?
# 지금은 응답의 구조가 단순하지만, 복잡하다면 미리 Response 객체를 분리하면,
# 더 유연하게 API 사용 가능

from pydantic import BaseModel
from typing import List

class ToDoSchema(BaseModel):
    id : int
    contents : str
    is_done : bool

    class Config:
        orm_mode = True
        # pydantic version 2보다 작아야 함
        # from_attributes  = True 원래 강의에는 없음
        # from_attributes=True

class ListToDoResponse(BaseModel):
    todos: List[ToDoSchema]


# from database.orm import ToDo
# todo = ToDo(id=100, contents='test', is_done=True)
# ToDoSchema.from_orm(todo)
# >>> ToDoSchema(id=100, contents='test', is_done=True)


