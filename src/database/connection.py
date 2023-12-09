from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:todos@127.0.0.1:3306/todos"

engine = create_engine(DATABASE_URL, echo=True)  #사용되는 시점의 sql문 print 되도록 echo= True
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

session = SessionFactory()

#session.query() #DB와 통신


# ORM 적용을 위해 generator 생성
# fastapi가 session 관리(처리) 할 수 있음
def get_db():
    session = SessionFactory()
    try:  #  session 사용
        yield session
    finally:  # session 사용 후에 session 삭제
        session.close()


