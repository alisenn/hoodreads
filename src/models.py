from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class Chapter:
    chapter_num: int
    title: str
    content: str
    key_takeaway: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Chapter":
        return cls(
            chapter_num=int(data["chapter_num"]),
            title=str(data["title"]),
            content=str(data["content"]).strip(),
            key_takeaway=str(data.get("key_takeaway", "")).strip(),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "chapter_num": self.chapter_num,
            "title": self.title,
            "content": self.content,
            "key_takeaway": self.key_takeaway,
        }


@dataclass
class Book:
    id: str
    title: str
    author: str
    tagline: str
    chapters: List[Chapter]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Book":
        chapters = [Chapter.from_dict(c) for c in data.get("chapters", [])]
        return cls(
            id=str(data["id"]),
            title=str(data["title"]),
            author=str(data["author"]),
            tagline=str(data.get("tagline", "")),
            chapters=chapters,
        )

    def get_chapter(self, chapter_num: int) -> Chapter | None:
        for ch in self.chapters:
            if ch.chapter_num == chapter_num:
                return ch
        return None

    @property
    def total_chapters(self) -> int:
        return len(self.chapters)
