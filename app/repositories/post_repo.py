from dataclasses import dataclass

from httpx import post

## 저장소 관리 역할을 수행하는 클래스이다.
## 저장할 데이터를 정의하고, 메모리 기반의 CRUD 기능을 제공한다.
@dataclass
class Post:
    id: int
    title: str
    content: str

class InMemoryPostRepository:
    def __init__(self):
        self._data: dict[int, Post] = {}
        self._seq: int = 1
    
    def save(self, title: str, content: str) -> Post:
        post = Post(id=self._seq, title=title, content=content)
        self._data[self._seq] = post
        self._seq += 1
        return post

    def find_all(self) -> list[Post]:
        return list(self._data.values())
    
    def find_by_id(self, post_id: int) -> Post | None:
        return self._data.get(post_id)
    
    def update(self, post_id: int, title: str | None, content: str | None) -> Post | None:
        post = self._data.get(post_id)
        if not post:
            return None
         
        if title is not None:
            post.title = title
        
        if content is not None:
            post.content = content
        return post

    def delete(self, post_id: int) -> bool:
        return self._data.pop(post_id, None) is not None