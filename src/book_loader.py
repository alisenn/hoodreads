import json
from pathlib import Path
from typing import Dict, List, Optional
from src.models import Book


class BookLoader:
    def __init__(self, books_dir: Optional[Path] = None):
        if books_dir is None:
            # Default to data/books relative to project root
            self.books_dir = Path(__file__).parent.parent / "data" / "books"
        else:
            self.books_dir = Path(books_dir)

    def load_all_books(self) -> Dict[str, Book]:
        books = {}
        if not self.books_dir.exists():
            return books

        for file_path in sorted(self.books_dir.glob("*.json")):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    book = Book.from_dict(data)
                    books[book.id] = book
            except Exception as e:
                print(f"[!] {file_path.name} yüklenirken hata: {e}")
        return books

    def get_book(self, book_id: str) -> Optional[Book]:
        books = self.load_all_books()
        return books.get(book_id)

    def save_book(self, book: Book) -> Path:
        self.books_dir.mkdir(parents=True, exist_ok=True)
        file_path = self.books_dir / f"{book.id}.json"
        data = {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "tagline": book.tagline,
            "chapters": [c.to_dict() for c in book.chapters],
        }
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return file_path
