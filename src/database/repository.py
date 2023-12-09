from sqlalchemy import select
from sqlalchemy.orm import Session
from database.orm import ToDo
from typing import List

# GET 전체 조회 API (DB통해서)
def get_todos(session: Session) -> List[ToDo]:
    return list(session.scalars(select(ToDo)))
