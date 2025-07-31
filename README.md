# 📚 Gutenberg Books API

A FastAPI-based REST API for accessing and filtering books from the Project Gutenberg dataset. Built for the Python Developer Internship assignment.

## ✅ Assignment Requirements Completed

### Core Features

- ✅ **All Filter Criteria**: `book_id`, `title`, `author`, `language`, `mime_type`, `topic`
- ✅ **Pagination**: 25 books per page with offset/limit support
- ✅ **Popularity Sorting**: Results ordered by `download_count` (descending)
- ✅ **Multiple Values**: Comma-separated values supported (e.g. `language=en,fr`)
- ✅ **Case-Insensitive Search**: Partial matching for `title`, `author`, and `topic`
- ✅ **JSON Response**: Structured response with `count` and `results` array

---

## 🧾 API Response Format

```json
{
  "count": 150,
  "results": [
    {
      "title": "Alice's Adventures in Wonderland",
      "download_count": 12345,
      "authors": ["Carroll, Lewis"],
      "languages": ["en"],
      "subjects": ["Children's stories", "Fantasy fiction"],
      "bookshelves": ["Children's Literature"],
      "formats": [
        {"mime_type": "text/html", "url": "https://..."},
        {"mime_type": "application/pdf", "url": "https://..."}
      ]
    }
  ]
}
```
---


## 🔧 Technology Stack

| Component      | Description                           |
|----------------|---------------------------------------|
| **FastAPI**    | Modern, fast (high-performance) web framework for building APIs with Python 3.6+ |
| **PostgreSQL** | Cloud-hosted database (NeonDB) used to store and query book metadata |
| **SQLAlchemy 2.0 (async)** | Fully async ORM for database models and queries |
| **Python 3.11+** | Latest Python version with async features |
---

### API Usage Examples

Basic search
```
GET /books?limit=10
```
Filter by multiple criteria
```
GET /books?language=en&topic=children&author=carroll
```
Multiple values per filter
```
GET /books?language=en,fr&topic=child,infant
```
Pagination
```
GET /books?limit=25&offset=50
```

### Quick Steup
```
git clone https://github.com/Aman140113/Gutenberg-Books-API.git
cd Gutenberg-Books-API
pip install -r requirements.txt
uvicorn main:app --reload
```
