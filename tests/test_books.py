import pytest
from src.book_loader import BookLoader
from src.formatter import CardFormatter


def test_books_exist_and_load():
    loader = BookLoader()
    books = loader.load_all_books()
    assert len(books) >= 6
    assert "ddia" in books
    assert "suc_ve_ceza" in books
    assert "donusum" in books
    assert "1984" in books
    assert "yabanci" in books
    assert "kucuk_prens" in books


def test_book_chapters_validity():
    loader = BookLoader()
    books = loader.load_all_books()

    for book_id, book in books.items():
        assert book.title, f"{book_id} başlığı eksik"
        assert book.author, f"{book_id} yazarı eksik"
        assert book.total_chapters > 0, f"{book_id} bölümü yok"

        for idx, ch in enumerate(book.chapters, start=1):
            assert ch.chapter_num == idx, f"{book_id} bölüm sıralaması hatalı: {ch.chapter_num} != {idx}"
            assert len(ch.content) > 20, f"{book_id} bölüm {ch.chapter_num} içeriği çok kısa"
            assert ch.key_takeaway, f"{book_id} bölüm {ch.chapter_num} ders notu eksik"


def test_all_chapters_format_cleanly():
    loader = BookLoader()
    books = loader.load_all_books()

    for book_id, book in books.items():
        for ch in book.chapters:
            card = CardFormatter.format_card(book, ch)
            assert card is not None
            plain = CardFormatter.format_plain(book, ch)
            assert book.title in plain
            assert ch.key_takeaway in plain
