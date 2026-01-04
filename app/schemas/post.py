from pydantic import BaseModel, Field

## dto 역할을 수행하는 파일이다.
## 요청과 응답에 주고받을 데이터의 구조를 정의한다.

class PostCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1, max_length=5000)

class PostUpdateRequest(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    content: str | None = Field(default=None, min_length=1, max_length=5000)

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    