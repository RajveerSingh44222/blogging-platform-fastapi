from datetime import date, datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

app = FastAPI(title="Inkflow Blogging API", version="1.0.0")


class BlogBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    excerpt: str = Field(..., min_length=10, max_length=400)
    content: str = Field(..., min_length=30)
    category: str = Field(..., examples=["design", "tech", "culture"])
    tag: str = Field(..., examples=["Design", "Tech", "Culture"])
    author: str = Field(..., min_length=2, max_length=100)
    read_time: str = Field(..., examples=["5 min"])
    publish_date: date
    likes: int = 0
    comments_count: int = 0
    is_published: bool = True


class BlogCreate(BlogBase):
    pass


class BlogUpdate(BaseModel):
    title: Optional[str] = None
    excerpt: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    tag: Optional[str] = None
    author: Optional[str] = None
    read_time: Optional[str] = None
    publish_date: Optional[date] = None
    likes: Optional[int] = None
    comments_count: Optional[int] = None
    is_published: Optional[bool] = None


class Blog(BlogBase):
    id: int
    created_at: datetime
    updated_at: datetime


class CommentCreate(BaseModel):
    name: str
    email: str
    content: str


blogs_db: List[Blog] = [
    Blog(
        id=1,
        title="The invisible hand: how great UX disappears into the product",
        excerpt="When design works, nobody notices it. That invisibility is the hardest thing to build.",
        content="Full content here...",
        category="design",
        tag="Design",
        author="Arjun Kumar",
        read_time="6 min",
        publish_date=date(2026, 3, 21),
        likes=2400,
        comments_count=118,
        is_published=True,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
]


def next_blog_id() -> int:
    return max((blog.id for blog in blogs_db), default=0) + 1


@app.get("/")
def root():
    return {"message": "Inkflow Blogging API is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/blogs", response_model=List[Blog])
def list_blogs(
    search: Optional[str] = Query(None, description="Search in title, excerpt, author, category, tag"),
    category: Optional[str] = None,
    tag: Optional[str] = None,
    author: Optional[str] = None,
    is_published: Optional[bool] = True,
):
    results = blogs_db

    if is_published is not None:
        results = [blog for blog in results if blog.is_published == is_published]
    if category:
        results = [blog for blog in results if blog.category.lower() == category.lower()]
    if tag:
        results = [blog for blog in results if blog.tag.lower() == tag.lower()]
    if author:
        results = [blog for blog in results if author.lower() in blog.author.lower()]
    if search:
        search_lower = search.lower()
        results = [
            blog for blog in results
            if search_lower in blog.title.lower()
            or search_lower in blog.excerpt.lower()
            or search_lower in blog.author.lower()
            or search_lower in blog.category.lower()
            or search_lower in blog.tag.lower()
        ]

    return results


@app.get("/blogs/{blog_id}", response_model=Blog)
def get_blog(blog_id: int):
    for blog in blogs_db:
        if blog.id == blog_id:
            return blog
    raise HTTPException(status_code=404, detail="Blog not found")


@app.post("/blogs", response_model=Blog, status_code=201)
def create_blog(payload: BlogCreate):
    blog = Blog(
        id=next_blog_id(),
        created_at=datetime.now(),
        updated_at=datetime.now(),
        **payload.model_dump(),
    )
    blogs_db.append(blog)
    return blog


@app.put("/blogs/{blog_id}", response_model=Blog)
def update_blog(blog_id: int, payload: BlogUpdate):
    for index, blog in enumerate(blogs_db):
        if blog.id == blog_id:
            updated_data = blog.model_dump()
            for key, value in payload.model_dump(exclude_unset=True).items():
                updated_data[key] = value
            updated_data["updated_at"] = datetime.now()
            updated_blog = Blog(**updated_data)
            blogs_db[index] = updated_blog
            return updated_blog
    raise HTTPException(status_code=404, detail="Blog not found")


@app.delete("/blogs/{blog_id}")
def delete_blog(blog_id: int):
    for index, blog in enumerate(blogs_db):
        if blog.id == blog_id:
            blogs_db.pop(index)
            return {"message": "Blog deleted successfully"}
    raise HTTPException(status_code=404, detail="Blog not found")


@app.get("/blogs/search", response_model=List[Blog])
def search_blogs(q: str = Query(..., min_length=1)):
    q_lower = q.lower()
    return [
        blog for blog in blogs_db
        if q_lower in blog.title.lower()
        or q_lower in blog.excerpt.lower()
        or q_lower in blog.author.lower()
        or q_lower in blog.category.lower()
        or q_lower in blog.tag.lower()
    ]


@app.get("/tags")
def list_tags():
    tags = sorted({blog.tag for blog in blogs_db})
    return {"tags": tags}


@app.get("/categories")
def list_categories():
    categories = sorted({blog.category for blog in blogs_db})
    return {"categories": categories}


@app.get("/authors")
def list_authors():
    authors = sorted({blog.author for blog in blogs_db})
    return {"authors": authors}


@app.post("/blogs/{blog_id}/like")
def like_blog(blog_id: int):
    for blog in blogs_db:
        if blog.id == blog_id:
            blog.likes += 1
            blog.updated_at = datetime.now()
            return {"message": "Blog liked", "likes": blog.likes}
    raise HTTPException(status_code=404, detail="Blog not found")


@app.post("/blogs/{blog_id}/comments")
def add_comment(blog_id: int, payload: CommentCreate):
    for blog in blogs_db:
        if blog.id == blog_id:
            blog.comments_count += 1
            blog.updated_at = datetime.now()
            return {
                "message": "Comment added successfully",
                "blog_id": blog_id,
                "comment": payload.model_dump(),
                "comments_count": blog.comments_count,
            }
    raise HTTPException(status_code=404, detail="Blog not found")


@app.get("/saved-posts")
def get_saved_posts(user_id: int = 1):
    return {"user_id": user_id, "saved_post_ids": [1, 3, 5]}


@app.post("/saved-posts/{blog_id}")
def save_post(blog_id: int, user_id: int = 1):
    return {"message": "Post saved successfully", "user_id": user_id, "blog_id": blog_id}


@app.delete("/saved-posts/{blog_id}")
def unsave_post(blog_id: int, user_id: int = 1):
    return {"message": "Post removed from saved list", "user_id": user_id, "blog_id": blog_id}


@app.get("/drafts")
def list_drafts(user_id: int = 1):
    return {"user_id": user_id, "drafts": []}


@app.post("/drafts")
def create_draft(payload: BlogCreate, user_id: int = 1):
    return {"message": "Draft created successfully", "user_id": user_id, "draft": payload.model_dump()}


@app.put("/drafts/{draft_id}")
def update_draft(draft_id: int, payload: BlogUpdate, user_id: int = 1):
    return {"message": "Draft updated successfully", "user_id": user_id, "draft_id": draft_id, "data": payload.model_dump(exclude_unset=True)}


@app.delete("/drafts/{draft_id}")
def delete_draft(draft_id: int, user_id: int = 1):
    return {"message": "Draft deleted successfully", "user_id": user_id, "draft_id": draft_id}
