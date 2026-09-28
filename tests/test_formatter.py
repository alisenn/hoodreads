import pytest
from src.models import Book, Chapter
from src.formatter import TweetFormatter


def test_short_chapter_single_tweet():
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
    tweets = TweetFormatter.format_thread(book, book.chapters[0])
    assert len(tweets) == 1
    assert "Test Kitap" in tweets[0]
    assert "Çaysız güne başlama." in tweets[0]
    assert TweetFormatter.calculate_length(tweets[0]) <= 280


def test_long_chapter_splits_to_thread():
    long_content = " ".join([
        "Bu birinci çok uzun ve detaylı sokak anlatımı cümlesidir.",
        "İkinci cümlede eleman kahveye gidip dayılarla okey oynamaya başlıyor.",
        "Üçüncü cümlede polis sirenleri çalınca herkes taşları gizleyip masadan kaçışıyor.",
        "Dördüncü cümlede ise bizimki mahallenin kedisini kucağına alıp hiçbir şey olmamış gibi ıslık çalıyor.",
        "Beşinci cümlede nihayet olay yerinden uzaklaşıp evine doğru yavaş adımlarla yol alıyor."
    ])
    book = Book(
        id="test_long",
        title="Uzun Test Kitabı",
        author="Yazar",
        tagline="Slogan",
        chapters=[
            Chapter(
                chapter_num=1,
                title="Bölüm 1: Baskın",
                content=long_content,
                key_takeaway="Polis gelince okeyi bozma.",
            )
        ]
    )
    tweets = TweetFormatter.format_thread(book, book.chapters[0])
    assert len(tweets) >= 1
    for t in tweets:
        assert TweetFormatter.calculate_length(t) <= 280
