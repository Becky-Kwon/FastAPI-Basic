# pip install fastapi  -> Uvicorn ASGI Server 를 사용
# ASGI (Asynchronous Server Gateway Interface)
# : 비동기 web server를 의미함 (DB나 API 연동 과정에서 발생하는 대기 시간을 낭비하지 않고, CPU가 다른 작업을 할 수 있도록 하는 방식)
# : async / await 구문을 사용
# pip install uvicorn  -> 4(매우 가벼운) ASGI 서버
# (fastapi framework만으로는 웹 개발을 할 수 없고, ASGI와 호환되는 웹 서버가 필요함)
# pip install pytest
# pip install httpx


from fastapi import FastAPI
from api import todo


app = FastAPI()
app.include_router(todo.router)


@app.get("/")  # root path로 get 요청

# 단순히 return 해줌
def health_check_handler():
    return {"ping" : "pong"}

# http://127.0.0.1:8000/docs => swaggerUI (docs 문서) 생성된거 확인 가능
# 웹 서버 실행 후 코드를 변경하면, 웹 서버를 재시작 해야 변경사항이 SwaggerUI에 반영됩니다.
# FastAPI 서버 종료 방법: Ctrl + C

