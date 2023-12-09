# ORM = ORM(Object-Relational Mapping)
# 관계형 데이터베이스를 객체 지향 프로그래밍(OOP)에 대응하여 사용하는 프로그래밍 기술
# 하나의 테이블 = 하나의 클래스
# 하나의 행(레코드) = 하나의 객체

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
