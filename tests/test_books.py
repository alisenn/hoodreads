import pytest
from src.book_loader import BookLoader
from src.formatter import TweetFormatter


def test_books_exist_and_load():
    loader = BookLoader()
    books = loader.load_all_books()
    assert len(books) >= 5
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


def test_all_chapters_fit_twitter_limit_or_thread():
    loader = BookLoader()
    books = loader.load_all_books()

    for book_id, book in books.items():
        for ch in book.chapters:
            tweets = TweetFormatter.format_thread(book, ch)
            assert 1 <= len(tweets) <= 3, f"{book_id} b{ch.chapter_num} tweet sayısı beklenenden fazla: {len(tweets)}"
            for idx, tweet_text in enumerate(tweets):
                char_count = TweetFormatter.calculate_length(tweet_text)
                assert char_count <= TweetFormatter.MAX_TWEET_LENGTH, (
                    f"{book_id} b{ch.chapter_num} tweet {idx + 1} uzunluğu sınırı aştı: {char_count} > 280\n"
                    f"İçerik: {tweet_text}"
                )
