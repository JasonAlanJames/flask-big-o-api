from flask import Flask, jsonify, request, g, has_request_context
from models import db, Author, Document
import random
from datetime import datetime, timedelta
import click
from sqlalchemy import Engine, event, select
from sqlalchemy.orm import selectinload
import time
from algorithms import bubble_sort, merge_sort

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///documents.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

@app.before_request
def reset_query_counter():
    g.sql_query_count = 0

@event.listens_for(Engine, "before_cursor_execute")
def count_sql_queries(
    conn,
    cursor,
    statement,
    parameters,
    context,
    executemany,
):
    if has_request_context():
        g.sql_query_count = getattr(
            g,
            "sql_query_count",
            0,
        ) + 1

@app.get("/api/health")
def health():
    return jsonify(
        {
            "status": "ok",
            "service": "Flask Big O API",
        }
    )

@app.get("/api/documents")
def get_documents():
    search_term = request.args.get(
        "q",
        default="",
        type=str,
    ).strip()

    sort_name = request.args.get(
        "sort",
        default="created_at",
        type=str,
    )

    order = request.args.get(
        "order",
        default="desc",
        type=str,
    ).lower()

    page = max(
        request.args.get("page", default=1, type=int),
        1,
    )

    page_size = request.args.get(
        "page_size",
        default=25,
        type=int,
    )

    page_size = max(1, min(page_size, 100))

    sortable_columns = {
        "id": Document.id,
        "title": Document.title,
        "created_at": Document.created_at,
        "author_id": Document.author_id,
    }

    sort_column = sortable_columns.get(sort_name)

    if sort_column is None:
        return jsonify(
            {
                "error": "Invalid sort field.",
                "allowed": list(sortable_columns.keys()),
            }
        ), 400

    if order not in {"asc", "desc"}:
        return jsonify(
            {
                "error": "order must be 'asc' or 'desc'."
            }
        ), 400

    statement = select(Document)

    if search_term:
        statement = statement.where(
            Document.title.contains(search_term)
            | Document.content.contains(search_term)
        )

    if order == "asc":
        statement = statement.order_by(
            sort_column.asc()
        )
    else:
        statement = statement.order_by(
            sort_column.desc()
        )

    offset = (page - 1) * page_size

    statement = statement.offset(offset).limit(page_size)

    documents = db.session.execute(
        statement
    ).scalars().all()

    return jsonify(
        {
            "query": search_term,
            "sort": sort_name,
            "order": order,
            "page": page,
            "page_size": page_size,
            "documents": [
                {
                    "id": document.id,
                    "title": document.title,
                    "author_id": document.author_id,
                    "created_at": document.created_at.isoformat(),
                }
                for document in documents
            ],
        }
    )

@app.post("/api/sort")
def sort_numbers():
    payload = request.get_json(silent=True) or {}

    numbers = payload.get("numbers")
    algorithm = payload.get("algorithm", "builtin")

    if not isinstance(numbers, list):
        return jsonify(
            {
                "error": "'numbers' must be an array."
            }
        ), 400

    if not all(
        isinstance(value, int) and not isinstance(value, bool)
        for value in numbers
    ):
        return jsonify(
            {
                "error": "Every value must be an  integer."
            }
        ), 400

    supported = {
        "builtin",
        "bubble",
        "merge",
    }

    if algorithm not in supported:
        return jsonify(
            {
                "error": "Unsupported algorithm.",
                "supported": sorted(supported),
            }
        ), 400

    if algorithm == "bubble" and len(numbers) > 10_000:
        return jsonify(
            {
                "error": (
                    "Bubble sort is limited to 10,000 values "
                    "because its worst-case complexity is O(n^2)."
                )
            }
        ), 400

    start = time.perf_counter_ns()

    comparisons = None
    swaps = None

    if algorithm == "bubble":
        result = bubble_sort(numbers)

        sorted_numbers = result.values
        comparisons = result.comparisons
        swaps = result.swaps

        complexity = {
            "best": "O(n)",
            "average": "O(n^2)",
            "worst": "O(n^2)",
        }

    elif algorithm == "merge":
        result = merge_sort(numbers)

        sorted_numbers = result.values
        comparisons = result.comparisons
        swaps = result.swaps

        complexity = {
            "best": "O(n log n)",
            "average": "O(n log n)",
            "worst": "O(n log n)",
        }

    else:
        sorted_numbers = sorted(numbers)

        complexity = {
            "best": "O(n)",
            "average": "O(n log n)",
            "worst": "O(n log n)",
            "implementation": "Python Timsort",
        }

    elapsed_ns = time.perf_counter_ns() - start

    return jsonify(
        {
            "algorithm": algorithm,
            "input_size": len(numbers),
            "complexity": complexity,
            "comparisons": comparisons,
            "swaps": swaps,
            "elapsed_nanoseconds": elapsed_ns,
            "result": sorted_numbers,
        }
    )

@app.get("/api/authors/n-plus-one")
def authors_n_plus_one():
    limit = request.args.get(
        "limit",
        default=20,
        type=int,
    )

    limit = max(1, min(limit, 100))

    authors = db.session.execute(
        select(Author).limit(limit)
    ).scalars().all()

    result = []

    for author in authors:
        documents = author.documents

        result.append(
            {
                "id": author.id,
                "name": author.name,
                "document_count": len(documents),
                "documents": [
                    {
                        "id": document.id,
                        "title": document.title,
                    }
                    for document in documents
                ],
            }
        )

    return jsonify(
        {
            "strategy": "N+1 lazy loading",
            "authors_returned": len(authors),
            "sql_queries": g.sql_query_count,
            "authors": result,
        }
    )

@app.get("/api/authors/optimized")
def authors_optimized():
    limit = request.args.get(
        "limit",
        default=20,
        type=int,
    )

    limit = max(1, min(limit, 100))

    statement = (
        select(Author)
        .options(
            selectinload(Author.documents)
        )
        .limit(limit)
    )

    authors = db.session.execute(
        statement
    ).scalars().all()

    result = []

    for author in authors:
        result.append(
            {
                "id": author.id,
                "name": author.name,
                "document_count": len(author.documents),
                "documents": [
                    {
                        "id": document.id,
                        "title": document.title,
                    }
                    for document in author.documents
                ],
            }
        )

    return jsonify(
    {
        "strategy": "selectinload eager loading",
        "authors_returned": len(authors),
        "sql_queries": g.sql_query_count,
        "authors": result,
    }
)

@app.cli.command("seed")
@click.option("--documents", default=5000, type=int)
@click.option("--authors", default=100, type=int)
def seed_database(documents: int, authors: int):
    db.drop_all()
    db.create_all()

    author_objects = [
        Author(
            name=f"Author {number:04d}"
        )
        for number in range(1, authors + 1)
    ]

    db.session.add_all(author_objects)
    db.session.flush()

    adjectives = [
        "Distributed",
        "Scalable",
        "Efficient",
        "Concurrent",
        "Reliable",
        "Modern",
        "Secure",
        "Indexed",
    ]

    subjects = [
        "Algorithms",
        "Databases",
        "APIs",
        "Documents",
        "Systems",
        "Search",
        "Sorting",
        "Architecture",
    ]

    base_date = datetime.utcnow()

    document_objects = []

    for number in range(1, documents + 1):
        adjective = random.choice(adjectives)
        subject = random.choice(subjects)
        author = random.choice(author_objects)

        document_objects.append(
            Document(
                title=f"{adjective} {subject} {number:06d}",
                content=(
                    f"Document {number} discussing "
                    f"{adjective.lower()} "
                    f"{subject.lower()}."
                ),
                created_at=(
                    base_date
                    - timedelta(
                        minutes=random.randint(
                            0,
                            500_000,
                        )
                    )
                ),
                author_id=author.id,
            )
        )

    db.session.add_all(document_objects)
    db.session.commit()

    click.echo(
        f"Created {authors} authors "
        f"and {documents} documents."
    )

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
    )