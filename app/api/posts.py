from fastapi import APIRouter
from app.schemas.post import PostCreateRequest, PostUpdateRequest, PostResponse
from app.app_state import post_service

# Controller의 역할을 수행한다.
# 라우팅을 정의하고, 관리하는 파일이다.

# JSON API는 /api 아래로 두고,
# 웹 페이지(HTML)는 /posts 등 별도 라우터에서 처리한다.
router = APIRouter(prefix="/api/posts", tags=["posts"])



@router.post("", response_model=PostResponse)
def create_post(req: PostCreateRequest):
    post = post_service.create(req.title, req.content)
    return PostResponse(id=post.id, title=post.title, content=post.content)

@router.get("", response_model=list[PostResponse])
def list_posts():
    posts = post_service.list()
    return [PostResponse(id=p.id, title=p.title, content=p.content) for p in posts]

@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int):
    p = post_service.get(post_id)
    return PostResponse(id=p.id, title=p.title, content=p.content)

@router.put("/{post_id}", response_model=PostResponse)
def update_post(post_id: int, req: PostUpdateRequest):
    p = post_service.update(post_id, req.title, req.content)
    return PostResponse(id=p.id, title=p.title, content=p.content)

@router.delete("/{post_id}")
def delete_post(post_id: int):
    post_service.delete(post_id)
    return {"ok": True}