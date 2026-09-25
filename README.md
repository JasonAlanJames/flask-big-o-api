# Flask Big-O & N+1 API

A Flask API project for practicing and demonstrating common software-engineering interview concepts involving:

* Big-O time complexity
* Bubble Sort
* Merge Sort
* Python Timsort
* Linear Search
* Binary Search
* Database filtering and sorting
* Pagination
* SQLAlchemy relationships
* The N+1 query problem
* Eager loading with `selectinload`
* SQL query counting
* REST API design

This project was built as a hands-on coding exercise rather than as a purely theoretical Big-O demonstration.

---

## Project Goals

The project demonstrates how algorithmic and database performance characteristics appear in real application code.

The main areas covered are:

### Sorting complexity

| Algorithm      |       Best |    Average |      Worst |
| -------------- | ---------: | ---------: | ---------: |
| Bubble Sort    |       O(n) |      O(n²) |      O(n²) |
| Merge Sort     | O(n log n) | O(n log n) | O(n log n) |
| Python Timsort |       O(n) | O(n log n) | O(n log n) |

### Search complexity

| Algorithm     | Complexity |
| ------------- | ---------: |
| Linear Search |       O(n) |
| Binary Search |   O(log n) |

### Database loading

The project also demonstrates the difference between:

```text
N+1 lazy loading
```

and:

```text
SQLAlchemy selectinload eager loading
```

In testing with 20 authors:

```text
N+1 version:
20 authors
21 SQL queries
```

while the optimized version required:

```text
20 authors
2 SQL queries
```

---

# Tech Stack

* Python
* Flask
* Flask-SQLAlchemy
* SQLAlchemy
* SQLite
* PowerShell
* Git
* GitHub

---

# Project Structure

```text
flask-big-o-api/
│
├── algorithms.py
├── app.py
├── models.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── instance/
│   └── documents.db
│
├── .venv/
└── __pycache__/
```

The following directories and files are intentionally excluded from Git:

```text
.venv/
instance/
__pycache__/
*.db
.env
```

---

# Files

## `app.py`

Contains the Flask application and REST API endpoints.

Responsibilities include:

* Flask configuration
* SQLAlchemy initialization
* SQL query counting
* document search
* document sorting
* pagination
* sorting API
* N+1 demonstration
* eager-loading optimization
* database seeding

---

## `models.py`

Contains the SQLAlchemy models.

The project currently includes:

### Author

```text
Author
├── id
├── name
└── documents
```

### Document

```text
Document
├── id
├── title
├── content
├── created_at
├── author_id
└── author
```

The relationship is deliberately configured to support demonstrating lazy loading and the N+1 query problem.

---

## `algorithms.py`

Contains manually implemented algorithms used for complexity analysis.

Currently includes:

```text
bubble_sort()
merge_sort()
linear_search()
binary_search()
```

Sorting functions return diagnostic information such as:

```text
sorted values
comparison count
swap count
```

This makes algorithm behavior observable instead of simply returning a sorted array.

---

# Installation

## 1. Clone the repository

```powershell
git clone https://github.com/JasonAlanJames/flask-big-o-api.git
```

Enter the project:

```powershell
cd flask-big-o-api
```

---

## 2. Create a virtual environment

```powershell
python -m venv .venv
```

Activate it in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution for the current session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Then activate again:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

## 3. Install dependencies

```powershell
pip install -r requirements.txt
```

Current primary dependencies:

```text
Flask
Flask-SQLAlchemy
```

---

# Database Setup

The application uses SQLite.

Database URI:

```text
sqlite:///documents.db
```

Flask-SQLAlchemy stores the SQLite database under the Flask instance directory.

Example:

```text
instance/documents.db
```

The database is intentionally excluded from Git.

---

# Seed the Database

The project includes a Flask CLI command that generates test data.

The default exercise dataset uses:

```text
100 authors
5,000 documents
```

Run:

```powershell
flask --app app seed --documents 5000 --authors 100
```

Expected output:

```text
Created 100 authors and 5000 documents.
```

The seed operation recreates the database tables before inserting the generated data.

---

# Start the API

Run:

```powershell
python app.py
```

The Flask development server starts at:

```text
http://127.0.0.1:5000
```

Example output:

```text
* Serving Flask app 'app'
* Debug mode: on
* Running on http://127.0.0.1:5000
```

> The Flask development server should not be used as a production WSGI server.

---

# API Endpoints

## Health Check

### Request

```http
GET /api/health
```

PowerShell:

```powershell
Invoke-RestMethod "http://127.0.0.1:5000/api/health"
```

Example response:

```json
{
  "service": "Flask Big O API",
  "status": "ok"
}
```

---

# Document Search, Sorting, and Pagination

## Endpoint

```http
GET /api/documents
```

Supported query parameters:

| Parameter   | Description              | Default      |
| ----------- | ------------------------ | ------------ |
| `q`         | Search title and content | empty        |
| `sort`      | Sort column              | `created_at` |
| `order`     | `asc` or `desc`          | `desc`       |
| `page`      | Page number              | `1`          |
| `page_size` | Results per page         | `25`         |

Maximum page size:

```text
100
```

Supported sort columns:

```text
id
title
created_at
author_id
```

---

## Example: Sort by Title

```powershell
Invoke-RestMethod "http://127.0.0.1:5000/api/documents?sort=title&order=asc&page_size=5"
```

---

## Example: Search Documents

```powershell
Invoke-RestMethod "http://127.0.0.1:5000/api/documents?q=Database&page_size=5"
```

Example request:

```http
GET /api/documents?q=Database&sort=created_at&order=desc&page=1&page_size=5
```

The filtering and ordering are performed by the database rather than by loading every record into Python first.

---

# Sorting API

## Endpoint

```http
POST /api/sort
```

Supported algorithms:

```text
bubble
merge
builtin
```

The `builtin` option uses Python's built-in `sorted()` implementation.

---

# Bubble Sort

Bubble Sort repeatedly compares neighboring values and swaps them when they are in the wrong order.

Average and worst-case time complexity:

```text
O(n²)
```

Example request:

```powershell
$body = @{
    algorithm = "bubble"
    numbers   = @(9,4,7,2,8,1,5,3,6)
} | ConvertTo-Json

Invoke-RestMethod `
    -Method Post `
    -Uri "http://127.0.0.1:5000/api/sort" `
    -ContentType "application/json" `
    -Body $body
```

Example result from the project:

```text
algorithm   : bubble
comparisons : 33
input_size  : 9
swaps       : 22
result      : 1,2,3,4,5,6,7,8,9
```

Complexity:

```text
Best:    O(n)
Average: O(n²)
Worst:   O(n²)
```

The API limits Bubble Sort requests to 10,000 values to prevent an intentionally inefficient algorithm from consuming excessive resources.

---

# Merge Sort

Merge Sort recursively divides the input and merges sorted subarrays.

Example:

```powershell
$body = @{
    algorithm = "merge"
    numbers   = @(9,4,7,2,8,1,5,3,6)
} | ConvertTo-Json
```

Then:

```powershell
Invoke-RestMethod `
    -Method Post `
    -Uri "http://127.0.0.1:5000/api/sort" `
    -ContentType "application/json" `
    -Body $body
```

Example project result:

```text
algorithm   : merge
comparisons : 21
input_size  : 9
swaps       : 0
result      : 1,2,3,4,5,6,7,8,9
```

Complexity:

```text
Best:    O(n log n)
Average: O(n log n)
Worst:   O(n log n)
```

---

# Python Built-In Sort

Python's built-in sorting implementation uses Timsort.

Example:

```powershell
$body = @{
    algorithm = "builtin"
    numbers   = @(9,4,7,2,8,1,5,3,6)
} | ConvertTo-Json
```

Then:

```powershell
Invoke-RestMethod `
    -Method Post `
    -Uri "http://127.0.0.1:5000/api/sort" `
    -ContentType "application/json" `
    -Body $body
```

Example response information:

```text
algorithm      : builtin
input_size     : 9
implementation : Python Timsort
result         : 1,2,3,4,5,6,7,8,9
```

Complexity:

```text
Best:    O(n)
Average: O(n log n)
Worst:   O(n log n)
```

The API does not report comparison or swap counts for Python's internal sort because `sorted()` does not expose those implementation details.

---

# Sorting Comparison

For the sample input:

```text
9,4,7,2,8,1,5,3,6
```

the manual implementations produced:

```text
Bubble Sort:
33 comparisons
22 swaps

Merge Sort:
21 comparisons
0 explicit swaps
```

As input size grows, the difference between:

```text
O(n²)
```

and:

```text
O(n log n)
```

becomes increasingly important.

---

# Linear Search

The project also contains a manual linear-search implementation.

Linear search checks elements sequentially.

Example test:

```python
linear_search(list(range(100)), 99)
```

Result:

```text
(99, 100)
```

Meaning:

```text
index found: 99
comparisons: 100
```

Complexity:

```text
O(n)
```

---

# Binary Search

Binary search repeatedly eliminates half of the remaining search space.

The collection must already be sorted.

Example:

```python
binary_search(list(range(100)), 99)
```

Result:

```text
(99, 7)
```

Meaning:

```text
index found: 99
comparisons: 7
```

Complexity:

```text
O(log n)
```

This provides a direct comparison:

```text
Linear Search:
100 comparisons

Binary Search:
7 comparisons
```

for the same 100-element sorted collection.

---

# N+1 Query Problem

One of the main database exercises in this project intentionally reproduces the N+1 query problem.

## Endpoint

```http
GET /api/authors/n-plus-one
```

Example:

```powershell
$result = Invoke-RestMethod "http://127.0.0.1:5000/api/authors/n-plus-one?limit=20"
```

Inspect:

```powershell
$result.strategy
$result.authors_returned
$result.sql_queries
```

Observed result:

```text
N+1 lazy loading
20
21
```

---

## Why 21 Queries?

First SQLAlchemy retrieves the authors:

```text
1 query
```

Then accessing:

```python
author.documents
```

causes another query for each author because the relationship uses lazy loading.

For 20 authors:

```text
1 author query
+
20 document queries
=
21 queries
```

Conceptually:

```sql
SELECT * FROM authors LIMIT 20;

SELECT * FROM documents WHERE author_id = 1;
SELECT * FROM documents WHERE author_id = 2;
SELECT * FROM documents WHERE author_id = 3;
...
SELECT * FROM documents WHERE author_id = 20;
```

This is the classic N+1 query problem.

---

# Optimized Relationship Loading

## Endpoint

```http
GET /api/authors/optimized
```

The optimized endpoint uses:

```python
selectinload(Author.documents)
```

Example:

```powershell
$result = Invoke-RestMethod "http://127.0.0.1:5000/api/authors/optimized?limit=20"
```

Then:

```powershell
$result.strategy
$result.authors_returned
$result.sql_queries
```

Observed result:

```text
selectinload eager loading
20
2
```

Instead of issuing one document query per author, SQLAlchemy retrieves the related documents in bulk.

The effective pattern becomes approximately:

```sql
SELECT *
FROM authors
LIMIT 20;
```

followed by:

```sql
SELECT *
FROM documents
WHERE author_id IN (...);
```

Result:

```text
N+1:
21 SQL queries

Optimized:
2 SQL queries
```

while returning the same logical author/document data.

---

# SQL Query Counter

The project registers a SQLAlchemy event listener using:

```text
before_cursor_execute
```

Each request resets:

```text
g.sql_query_count
```

and increments it each time SQLAlchemy executes a SQL statement.

This makes the N+1 problem directly measurable from API responses.

---

# Big-O Summary

The project demonstrates the following complexity classes:

```text
O(1)
Constant time

O(log n)
Binary search

O(n)
Linear search

O(n log n)
Merge sort
Efficient general-purpose sorting

O(n²)
Bubble sort
Nested-loop-style growth
```

A useful mental model is:

```text
Dictionary lookup
    ↓
   O(1)

Binary search
    ↓
O(log n)

Single traversal
    ↓
   O(n)

Efficient sorting
    ↓
O(n log n)

Nested traversal
    ↓
  O(n²)
```

---

# Interview Concepts Demonstrated

This project can be used to practice explaining several common software-engineering interview topics.

## Algorithm questions

* What is Big-O notation?
* What is the difference between O(n) and O(log n)?
* Why must binary search operate on sorted data?
* Why is Bubble Sort inefficient for large inputs?
* Why is Merge Sort O(n log n)?
* What is the tradeoff between Merge Sort time and auxiliary memory?

## Backend questions

* How should an API validate user input?
* How should sorting fields be restricted?
* Why should pagination have a maximum page size?
* Why should filtering and sorting generally happen in the database?
* What is the N+1 query problem?
* How do lazy loading and eager loading differ?
* How can SQLAlchemy's `selectinload()` reduce database queries?

## Database questions

* What is a foreign key?
* What is an ORM relationship?
* What is lazy loading?
* What is eager loading?
* Why do indexes matter?
* How can query count affect application scalability?

---

# Example Interview Explanation

A concise explanation of the N+1 issue demonstrated by this project:

> The N+1 query problem happens when an application first queries a collection of parent records and then performs an additional query for every parent's related records. In this project, retrieving 20 authors and lazily accessing each author's documents caused 21 SQL queries. Using SQLAlchemy's `selectinload()` reduced the same operation to two queries by retrieving the related documents in bulk.

A concise Big-O explanation:

> Big-O describes how an algorithm's work grows as input size grows. Linear search is O(n) because it may inspect every value. Binary search is O(log n) because each comparison eliminates approximately half of the remaining search space. Bubble Sort is O(n²) in its average and worst cases, while Merge Sort is O(n log n).

---

# Development Workflow

Activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Start Flask:

```powershell
python app.py
```

Seed or reset test data:

```powershell
flask --app app seed --documents 5000 --authors 100
```

Check Git:

```powershell
git status
```

---

# Git Workflow

After making changes:

```powershell
git add .
```

Review:

```powershell
git status
```

Commit:

```powershell
git commit -m "Describe the change"
```

Push:

```powershell
git push origin main
```

---

# Security and Production Notes

This repository is designed primarily as a development and interview-practice project.

For a production deployment, additional considerations would include:

* disabling Flask debug mode
* using a production WSGI server
* using environment-based configuration
* replacing SQLite where higher concurrency is required
* implementing authentication and authorization
* implementing structured logging
* adding rate limiting
* validating request sizes
* adding automated tests
* adding database migrations
* adding monitoring and observability

Sensitive values and `.env` files should never be committed to Git.

---

# Potential Future Improvements

Possible extensions include:

* expose linear search through `/api/search/linear`
* expose binary search through `/api/search/binary`
* benchmark larger input sizes
* compare algorithm execution times
* add Quick Sort
* add Heap Sort
* add hash-table lookup examples
* add full-text database search
* add database query plans
* compare indexed versus non-indexed queries
* add unit tests with `pytest`
* add API integration tests
* add Docker support
* add PostgreSQL support
* add Swagger / OpenAPI documentation
* add CI with GitHub Actions

---

# Repository

GitHub:

```text
https://github.com/JasonAlanJames/flask-big-o-api
```

---

# Author

Jason Alan James

---

## License

This project is licensed under the MIT License.

See the `LICENSE` file for details.
