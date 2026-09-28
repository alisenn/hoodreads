from rich.panel import Panel
from rich.text import Text
from src.models import Book, Chapter


class CardFormatter:
    @classmethod
    def format_card(cls, book: Book, chapter: Chapter) -> Panel:
        """
        Creates a rich, aesthetic terminal card for reading a chapter/sub-topic.
        """
        header_text = f"[bold cyan]{book.title}[/] [dim]— {book.author}[/]\n"
        progress_text = f"[bold yellow]Bölüm {chapter.chapter_num} / {book.total_chapters}[/]\n\n"
        title_text = f"[bold white on blue] 📌 {chapter.title} [/]\n\n"
        content_text = f"[bold white]{chapter.content}[/]\n\n"
        footer_text = f"[bold yellow]💡 Sokak Dersi:[/] [italic green]{chapter.key_takeaway}[/]"

        full_text = f"{header_text}{progress_text}{title_text}{content_text}{footer_text}"

        return Panel(
            full_text,
            title=f"💀 HoodReads | {chapter.chapter_num}/{book.total_chapters}",
            subtitle=f"{book.title}",
            border_style="magenta",
            padding=(1, 2),
        )

    @classmethod
    def format_plain(cls, book: Book, chapter: Chapter) -> str:
        """
        Plain text representation for logging or piping.
        """
        return (
            f"📖 {book.title} ({chapter.chapter_num}/{book.total_chapters})\n"
            f"📌 {chapter.title}\n\n"
            f"{chapter.content}\n\n"
            f"💡 Sokak Dersi: {chapter.key_takeaway}"
        )
