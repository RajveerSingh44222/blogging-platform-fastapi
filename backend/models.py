from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class BlogBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    subtitle: str | None = Field(None, max_length=500)
    content: str = Field(..., min_length=20)
    author: str = Field(..., min_length=2, max_length=100)
    category: str = Field(..., min_length=2, max_length=100)
    tags: str | None = Field(None, max_length=255)
    cover_image: str | None = Field(None, max_length=500)
    read_time: str | None = Field(None, max_length=50)
    is_published: bool = True


class BlogCreate(BlogBase):
    pass


class BlogUpdate(BaseModel):
    title: str | None = Field(None, min_length=3, max_length=255)
    subtitle: str | None = Field(None, max_length=500)
    content: str | None = Field(None, min_length=20)
    author: str | None = Field(None, min_length=2, max_length=100)
    category: str | None = Field(None, min_length=2, max_length=100)
    tags: str | None = Field(None, max_length=255)
    cover_image: str | None = Field(None, max_length=500)
    read_time: str | None = Field(None, max_length=50)
    is_published: bool | None = None


class BlogResponse(BlogBase):
    id: int
    publish_date: datetime
    likes: int
    comments_count: int

    model_config = ConfigDict(from_attributes=True)


class CommentCreate(BaseModel):
    commenter_name: str = Field(..., min_length=2, max_length=100)
    comment_text: str = Field(..., min_length=1)


class CommentResponse(BaseModel):
    id: int
    blog_id: int
    commenter_name: str
    comment_text: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SavedPostCreate(BaseModel):
    saved_by: str = Field(default="guest", min_length=1, max_length=100)


class SavedPostResponse(BaseModel):
    id: int
    blog_id: int
    saved_by: str
    saved_at: datetime

    model_config = ConfigDict(from_attributes=True)