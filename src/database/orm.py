from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

#
# docker에서 만든 todos DB랑 똑같이 만들기
#
class ToDo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key= True, index=True)
    contents = Column(String(256), nullable=False)
    is_done = Column(Boolean, nullable=False)

    def __repr__(self):
        return f"ToDo(id={self.id}, contents={self.contents}, is_done={self.is_done})"
