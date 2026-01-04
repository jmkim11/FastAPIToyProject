from __future__ import annotations

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.app_state import post_service


router = APIRouter(tags=["web"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    # 기본 페이지는 목록으로
    return RedirectResponse(url="/posts", status_code=302)


@router.get("/posts", response_class=HTMLResponse)
def posts_list(request: Request):
    posts = post_service.list()
    return templates.TemplateResponse(
        "posts_list.html",
        {"request": request, "posts": posts},
    )


@router.get("/posts/new", response_class=HTMLResponse)
def posts_new_form(request: Request):
    return templates.TemplateResponse(
        "post_form.html",
        {
            "request": request,
            "mode": "create",
            "post": None,
        },
    )


@router.post("/posts/new")
def posts_create(title: str = Form(...), content: str = Form(...)):
    post_service.create(title, content)
    return RedirectResponse(url="/posts", status_code=302)


@router.get("/posts/{post_id}", response_class=HTMLResponse)
def posts_detail(request: Request, post_id: int):
    post = post_service.get(post_id)
    return templates.TemplateResponse(
        "post_detail.html",
        {"request": request, "post": post},
    )


@router.get("/posts/{post_id}/edit", response_class=HTMLResponse)
def posts_edit_form(request: Request, post_id: int):
    post = post_service.get(post_id)
    return templates.TemplateResponse(
        "post_form.html",
        {
            "request": request,
            "mode": "edit",
            "post": post,
        },
    )


@router.post("/posts/{post_id}/edit")
def posts_update(post_id: int, title: str = Form(...), content: str = Form(...)):
    post_service.update(post_id, title=title, content=content)
    return RedirectResponse(url=f"/posts/{post_id}", status_code=302)


@router.post("/posts/{post_id}/delete")
def posts_delete(post_id: int):
    post_service.delete(post_id)
    return RedirectResponse(url="/posts", status_code=302)
