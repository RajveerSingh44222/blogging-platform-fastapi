from fastapi import FastAPI, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi.middleware.cors import CORSMiddleware

from database import engine, get_db
from database_model import Base, Blog as DBBlog, Comment as DBComment, SavedPost as DBSavedPost
from models import (
    BlogCreate,
    BlogUpdate,
    BlogResponse,
    CommentCreate,
    CommentResponse,
    SavedPostCreate,
    SavedPostResponse,
)

app = FastAPI(
    title="Blogging Platform API",
    description="A FastAPI backend for a blogging platform using SQLAlchemy and MySQL.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables automatically
Base.metadata.create_all(bind=engine)


@app.get("/", tags=["Home"])
def root():
    return {"message": "Blogging Platform API is running"}


@app.get("/health", tags=["Home"])
def health_check():
    return {"status": "healthy"}


# ---------------- BLOG ROUTES ----------------

@app.post(
    "/blogs",
    response_model=BlogResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Blogs"]
)
def create_blog(blog: BlogCreate, db: Session = Depends(get_db)):
    try:
        db_blog = DBBlog(**blog.model_dump())
        db.add(db_blog)
        db.commit()
        db.refresh(db_blog)
        return db_blog
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create blog: {str(e)}"
        )


@app.get(
    "/blogs",
    response_model=list[BlogResponse],
    tags=["Blogs"]
)
def get_all_blogs(
    search: str | None = Query(None, description="Search by title, author, category, or tags"),
    category: str | None = Query(None, description="Filter by category"),
    author: str | None = Query(None, description="Filter by author"),
    is_published: bool | None = Query(None, description="Filter published/draft blogs"),
    sort_by: str = Query("publish_date", description="Sort by: id, title, author, publish_date, likes, comments_count"),
    order: str = Query("desc", description="Sort order: asc or desc"),
    db: Session = Depends(get_db)
):
    query = db.query(DBBlog)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                DBBlog.title.like(search_term),
                DBBlog.author.like(search_term),
                DBBlog.category.like(search_term),
                DBBlog.tags.like(search_term)
            )
        )

    if category:
        query = query.filter(DBBlog.category == category)

    if author:
        query = query.filter(DBBlog.author == author)

    if is_published is not None:
        query = query.filter(DBBlog.is_published == is_published)

    allowed_sort_fields = {
        "id": DBBlog.id,
        "title": DBBlog.title,
        "author": DBBlog.author,
        "publish_date": DBBlog.publish_date,
        "likes": DBBlog.likes,
        "comments_count": DBBlog.comments_count
    }

    if sort_by not in allowed_sort_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid sort_by field."
        )

    column = allowed_sort_fields[sort_by]

    if order.lower() == "desc":
        query = query.order_by(column.desc())
    elif order.lower() == "asc":
        query = query.order_by(column.asc())
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid order value. Use asc or desc."
        )

    return query.all()


@app.get(
    "/blogs/{blog_id}",
    response_model=BlogResponse,
    tags=["Blogs"]
)
def get_blog_by_id(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(DBBlog).filter(DBBlog.id == blog_id).first()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found"
        )

    return blog


@app.put(
    "/blogs/{blog_id}",
    response_model=BlogResponse,
    tags=["Blogs"]
)
def update_blog(blog_id: int, blog: BlogUpdate, db: Session = Depends(get_db)):
    existing_blog = db.query(DBBlog).filter(DBBlog.id == blog_id).first()

    if not existing_blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found"
        )

    try:
        update_data = blog.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(existing_blog, key, value)

        db.commit()
        db.refresh(existing_blog)
        return existing_blog

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update blog: {str(e)}"
        )


@app.delete(
    "/blogs/{blog_id}",
    tags=["Blogs"]
)
def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(DBBlog).filter(DBBlog.id == blog_id).first()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found"
        )

    try:
        db.delete(blog)
        db.commit()
        return {"message": "Blog deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete blog: {str(e)}"
        )


@app.post(
    "/blogs/{blog_id}/like",
    tags=["Blogs"]
)
def like_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(DBBlog).filter(DBBlog.id == blog_id).first()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found"
        )

    try:
        blog.likes += 1
        db.commit()
        db.refresh(blog)
        return {
            "message": "Blog liked successfully",
            "blog_id": blog.id,
            "total_likes": blog.likes
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to like blog: {str(e)}"
        )


# ---------------- COMMENT ROUTES ----------------

@app.post(
    "/blogs/{blog_id}/comments",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Comments"]
)
def add_comment(blog_id: int, comment: CommentCreate, db: Session = Depends(get_db)):
    blog = db.query(DBBlog).filter(DBBlog.id == blog_id).first()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found"
        )

    try:
        db_comment = DBComment(
            blog_id=blog_id,
            commenter_name=comment.commenter_name,
            comment_text=comment.comment_text
        )
        db.add(db_comment)

        blog.comments_count += 1

        db.commit()
        db.refresh(db_comment)
        return db_comment

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add comment: {str(e)}"
        )


@app.get(
    "/blogs/{blog_id}/comments",
    response_model=list[CommentResponse],
    tags=["Comments"]
)
def get_blog_comments(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(DBBlog).filter(DBBlog.id == blog_id).first()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found"
        )

    return db.query(DBComment).filter(DBComment.blog_id == blog_id).all()


# ---------------- SAVED POSTS ROUTES ----------------

@app.post(
    "/saved-posts/{blog_id}",
    response_model=SavedPostResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Saved Posts"]
)
def save_post(blog_id: int, payload: SavedPostCreate, db: Session = Depends(get_db)):
    blog = db.query(DBBlog).filter(DBBlog.id == blog_id).first()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found"
        )

    existing_saved = db.query(DBSavedPost).filter(
        DBSavedPost.blog_id == blog_id,
        DBSavedPost.saved_by == payload.saved_by
    ).first()

    if existing_saved:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Post already saved by this user"
        )

    try:
        saved_post = DBSavedPost(
            blog_id=blog_id,
            saved_by=payload.saved_by
        )
        db.add(saved_post)
        db.commit()
        db.refresh(saved_post)
        return saved_post

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save post: {str(e)}"
        )


@app.get(
    "/saved-posts",
    response_model=list[SavedPostResponse],
    tags=["Saved Posts"]
)
def get_saved_posts(
    saved_by: str = Query("guest", description="Username of the saver"),
    db: Session = Depends(get_db)
):
    return db.query(DBSavedPost).filter(DBSavedPost.saved_by == saved_by).all()


@app.delete(
    "/saved-posts/{blog_id}",
    tags=["Saved Posts"]
)
def remove_saved_post(
    blog_id: int,
    saved_by: str = Query("guest"),
    db: Session = Depends(get_db)
):
    saved_post = db.query(DBSavedPost).filter(
        DBSavedPost.blog_id == blog_id,
        DBSavedPost.saved_by == saved_by
    ).first()

    if not saved_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Saved post not found"
        )

    try:
        db.delete(saved_post)
        db.commit()
        return {"message": "Saved post removed successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to remove saved post: {str(e)}"
        )

  