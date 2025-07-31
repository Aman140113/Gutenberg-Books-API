# Gutenberg-Books-API

A FastAPI-based backend that exposes a REST API for accessing and filtering books from the Project Gutenberg dataset stored in a NeonDB (PostgreSQL-compatible) database.

---

## 🚀 Features

- Filter books by:
  - `book_id`
  - `title`
  - `author`
  - `language`
  - `mime_type`
  - `topic` (matches both subject and bookshelf)
- Pagination support with `offset` and `limit` (returns 25 books per page by default)
- Results ordered by `download_count` (descending)
- Asynchronous database queries for high performance
- OpenAPI docs auto-generated at `/docs`

---

## 🛠️ Tech Stack

- **Python 3.11+**
- **FastAPI** – Web framework
- **SQLAlchemy 2.0 (async)** – ORM
- **PostgreSQL (NeonDB)** – Cloud-hosted database
- **asyncpg** – Async PostgreSQL driver
- **Pydantic v2** – Data validation and serialization

---

## 📦 Project Structure
gutenberg_api/
├── main.py # Main FastAPI app
├── requirements.txt # Required dependencies
├── .env # Environment variables (not included in version control)
├── README.md # This file

## 📄 Requirements

Install dependencies:

```bash
pip install -r requirements.txt
