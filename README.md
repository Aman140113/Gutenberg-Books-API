Gutenberg Books API
A FastAPI-based REST API for accessing and filtering books from the Project Gutenberg dataset. Built for the Python Developer Internship assignment.
🚀 Live Demo

API URL: [Your deployed URL here]
Interactive Documentation: [Your deployed URL]/docs

## Assignment Requirements Completed
- Core Features

✅ All Filter Criteria: book_id, title, author, language, mime_type, topic
✅ Pagination: 25 books per page with offset/limit support
✅ Popularity Sorting: Results ordered by download count (descending)
✅ Multiple Values: Support for comma-separated filter values (language=en,fr)
✅ Case-Insensitive Search: Partial matching for title, author, and topic
✅ JSON Response: Structured response with count and results array

## API Response Format
json{
  "count": 150,
  "results": [
    {
      "id": 11,
      "title": "Alice's Adventures in Wonderland",
      "author": "Carroll, Lewis",
      "genre": "Fiction",
      "language": "en",
      "subjects": ["Children's stories", "Fantasy fiction"],
      "bookshelves": ["Children's Literature"],
      "download_links": [
        {"format": "text/html", "url": "..."},
        {"format": "application/pdf", "url": "..."}
      ]
    }
  ]
}

## 🔧 Technology Stack

- FastAPI - Modern Python web framework
- SQLAlchemy 2.0 (async) - Database ORM with async support
- PostgreSQL (NeonDB) - Cloud-hosted database
- Python 3.11+ - Latest Python version

## 📋 API Usage Examples
'''bash Basic search
GET /books?limit=10
# Filter by multiple criteria
GET /books?language=en&topic=children&author=carroll
# Multiple values per filter
GET /books?language=en,fr&topic=child,infant
# Pagination
GET /books?limit=25&offset=50


🚀 Quick Setup
bash'''
git clone https://github.com/Aman140113/Gutenberg-Books-API.git
cd Gutenberg-Books-API
pip install -r requirements.txt
uvicorn main:app --reload
