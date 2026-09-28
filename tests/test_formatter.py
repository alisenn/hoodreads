import pytest
from src.models import Book, Chapter
from src.formatter import CardFormatter


def test_card_formatter():
    book = Book(
        id="test_book",
        title="Test Kitap",
        author="Test Yazar",
        tagline="Test slogan",
        chapters=[
            Chapter(
                chapter_num=1,
                title="Bölüm 1",
                content="Eleman sabah uyanıyor. Çayını koyuyor, sokağa çıkıyor.",
                key_takeaway="Çaysız güne başlama.",
            )
        ]
    )
    card = CardFormatter.format_card(book, book.chapters[0])
    assert card is not None

    plain = CardFormatter.format_plain(book, book.chapters[0])
    assert "Test Kitap" in plain
    assert "Çaysız güne başlama." in plain
