import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional
from src.book_loader import BookLoader


class StateManager:
    def __init__(self, state_file: Optional[Path] = None, book_loader: Optional[BookLoader] = None):
        if state_file is None:
            self.state_file = Path(__file__).parent.parent / "data" / "state.json"
        else:
            self.state_file = Path(state_file)
        self.book_loader = book_loader or BookLoader()

    def _default_state(self) -> Dict[str, Any]:
        books = self.book_loader.load_all_books()
        first_book_id = "ddia" if "ddia" in books else (next(iter(books.keys())) if books else "")
        return {
            "current_book_id": first_book_id,
            "current_chapter_num": 1,
            "history": [],
            "last_read_at": None,
        }

    def load_state(self) -> Dict[str, Any]:
        if not self.state_file.exists():
            state = self._default_state()
            self.save_state(state)
            return state

        try:
            with open(self.state_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            state = self._default_state()
            self.save_state(state)
            return state

    def save_state(self, state: Dict[str, Any]) -> None:
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)

    def set_active_book(self, book_id: str, chapter_num: int = 1) -> bool:
        book = self.book_loader.get_book(book_id)
        if not book:
            return False
        state = self.load_state()
        state["current_book_id"] = book_id
        state["current_chapter_num"] = max(1, min(chapter_num, book.total_chapters))
        self.save_state(state)
        return True

    def get_current(self) -> Optional[Dict[str, Any]]:
        state = self.load_state()
        book_id = state.get("current_book_id")
        chapter_num = state.get("current_chapter_num", 1)

        book = self.book_loader.get_book(book_id) if book_id else None
        if not book:
            books = self.book_loader.load_all_books()
            if not books:
                return None
            book = next(iter(books.values()))
            book_id = book.id
            chapter_num = 1
            state["current_book_id"] = book_id
            state["current_chapter_num"] = 1
            self.save_state(state)

        chapter = book.get_chapter(chapter_num)
        if not chapter:
            chapter = book.chapters[0] if book.chapters else None
            if not chapter:
                return None

        return {
            "book": book,
            "chapter": chapter,
            "is_last_chapter": chapter_num >= book.total_chapters,
        }

    def advance(self) -> Dict[str, Any]:
        state = self.load_state()
        book_id = state["current_book_id"]
        chapter_num = state["current_chapter_num"]

        now = datetime.now(timezone.utc).isoformat()
        state["history"].append({
            "book_id": book_id,
            "chapter_num": chapter_num,
            "read_at": now,
        })
        state["last_read_at"] = now

        books = self.book_loader.load_all_books()
        book = books.get(book_id)
        book_ids = list(books.keys())

        if book and chapter_num < book.total_chapters:
            state["current_chapter_num"] = chapter_num + 1
        else:
            # Switch to next book
            if book_ids and book_id in book_ids:
                curr_idx = book_ids.index(book_id)
                next_idx = (curr_idx + 1) % len(book_ids)
                state["current_book_id"] = book_ids[next_idx]
            elif book_ids:
                state["current_book_id"] = book_ids[0]
            state["current_chapter_num"] = 1

        self.save_state(state)
        return state

    def previous(self) -> Dict[str, Any]:
        state = self.load_state()
        chapter_num = state.get("current_chapter_num", 1)
        if chapter_num > 1:
            state["current_chapter_num"] = chapter_num - 1
            self.save_state(state)
        return state
