from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False, index=True)
    subtitle = Column(String(500), nullable=True)
    content = Column(Text, nullable=False)
    author = Column(String(100), nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)
    tags = Column(String(255), nullable=True)  # comma-separated tags
    cover_image = Column(String(500), nullable=True)

    publish_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    read_time = Column(String(50), nullable=True)
    likes = Column(Integer, default=0, nullable=False)
    comments_count = Column(Integer, default=0, nullable=False)
    is_published = Column(Boolean, default=True, nullable=False)

    comments = relationship(
        "Comment",
        back_populates="blog",
        cascade="all, delete-orphan"
    )
    saved_by = relationship(
        "SavedPost",
        back_populates="blog",
        cascade="all, delete-orphan"
    )


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    blog_id = Column(Integer, ForeignKey("blogs.id", ondelete="CASCADE"), nullable=False)
    commenter_name = Column(String(100), nullable=False)
    comment_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    blog = relationship("Blog", back_populates="comments")


class SavedPost(Base):
    __tablename__ = "saved_posts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    blog_id = Column(Integer, ForeignKey("blogs.id", ondelete="CASCADE"), nullable=False)
    saved_by = Column(String(100), nullable=False, default="guest")
    saved_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    blog = relationship("Blog", back_populates="saved_by")