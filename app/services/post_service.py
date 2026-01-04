from fastapi import HTTPException, status
from app.repositories.post_repo import InMemoryPostRepository, Post

class PostService:
    def __init__(self, repository: InMemoryPostRepository):
        self.repository = repository
    
    def create(self, title: str, content: str) -> Post:
        return self.repository.save(title, content)
    
    def list(self) -> list[Post]:
        return self.repository.find_all()
    
    def get(self, post_id: int) -> Post:
        post = self.repository.find_by_id(post_id)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        return post
    
    def update(self, post_id: int, title: str | None, content: str | None) -> Post | None:
        post = self.repository.update(post_id, title, content)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        return post
    
    def delete(self, post_id: int) -> None:
        deleted = self.repository.delete(post_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        