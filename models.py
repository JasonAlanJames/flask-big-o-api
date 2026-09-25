from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = "authors"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    name = db.Column(
        db.String(200),
        nullable=False,
        index=True,
    )

    documents = db.relationship(
        "Document",
        back_populates="author",
        lazy="select",
    )

class Document(db.Model):
    __tablename__ = "documents"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    title = db.Column(
        db.String(255),
        nullable=False,
        index=True,
    )

    content = db.Column(
        db.Text,
        nullable=False,
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        index=True,
    )

    author_id = db.Column(
        db.Integer,
        db.ForeignKey("authors.id"),
        nullable=False,
        index=True,
    )

    author = db.relationship(
        "Author",
        back_populates="documents",
    )