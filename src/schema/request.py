# Refactoring 
# CreateToDoRequest 모듈을 main 에서 가져옴
from pydantic import BaseModel

class CreateToDoRequest(BaseModel):
    id : int
    contents : str
    is_done : bool