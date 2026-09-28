import argparse
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt

from src.book_loader import BookLoader
from src.state_manager import StateManager
from src.formatter import CardFormatter

console = Console()


def cmd_list(args):
    loader = BookLoader()
    books = loader.load_all_books()
    state_mgr = StateManager(book_loader=loader)
    state = state_mgr.load_state()

    active_id = state.get("current_book_id")
    curr_chapter = state.get("current_chapter_num", 1)

    table = Table(title="💀 HoodReads — Kişisel Sokak Kitaplığın", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="cyan", width=14)
    table.add_column("Kitap Adı", style="bold green", width=24)
    table.add_column("Yazar", style="yellow", width=18)
    table.add_column("Alt Başlıklar", justify="center", width=14)
    table.add_column("İlerleme", style="bold", width=20)

    for b_id, book in books.items():
        if b_id == active_id:
            status = f"[bold green]▶ Okunuyor ({curr_chapter}/{book.total_chapters})[/]"
        else:
            status = "[dim]Kütüphanede[/]"
        table.add_row(book.id, book.title, book.author, f"{book.total_chapters} parça", status)

    console.print(table)
    console.print("\n[dim]İpucu: Okumaya başlamak için:[/] [bold cyan]python main.py read[/] [dim]veya interaktif mod için:[/] [bold green]python main.py interactive[/]\n")


def cmd_preview(args):
    loader = BookLoader()
    book = loader.get_book(args.book_id)
    if not book:
        console.print(f"[bold red]Hata:[/] '{args.book_id}' id'li kitap bulunamadı.")
        return

    console.print(Panel(
        f"[bold yellow]{book.title}[/] - {book.author}\n[italic]{book.tagline}[/]\nToplam Alt Başlık / Konu: [bold cyan]{book.total_chapters}[/]",
        title="📖 Kitap Detayı",
        border_style="cyan"
    ))

    chapters = book.chapters
    if getattr(args, "chapter", None):
        prefix = f"{args.chapter}."
        filtered = [c for c in chapters if c.title.startswith(prefix) or f"Bölüm {args.chapter}:" in c.title or c.chapter_num == args.chapter]
        if filtered:
            chapters = filtered

    if getattr(args, "limit", None) and args.limit > 0:
        chapters = chapters[:args.limit]

    for ch in chapters:
        card = CardFormatter.format_card(book, ch)
        console.print(card)


def cmd_read(args):
    loader = BookLoader()
    state_mgr = StateManager(book_loader=loader)
    curr = state_mgr.get_current()

    if not curr:
        console.print("[bold red]Hata:[/] Okunacak kitap bulunamadı.")
        return

    book = curr["book"]
    chapter = curr["chapter"]

    card = CardFormatter.format_card(book, chapter)
    console.print(card)

    state_mgr.advance()
    next_task = state_mgr.get_current()
    if next_task:
        console.print(f"[dim]Sıradaki: {next_task['book'].title} -> {next_task['chapter'].title}[/]\n")


def cmd_interactive(args):
    loader = BookLoader()
    state_mgr = StateManager(book_loader=loader)

    console.print(Panel(
        "[bold cyan]💀 HoodReads İnteraktif Okuyucu[/]\n"
        "[dim]Sıkılmadan, 3-4 sayfalık alt başlıklarla adım adım kitap oku.[/]\n\n"
        "Komutlar:\n"
        "  [bold green]Enter / 'n'[/] : Sıradaki alt başlık\n"
        "  [bold yellow]'p'[/]         : Önceki alt başlık\n"
        "  [bold red]'q'[/]         : Çıkış",
        border_style="cyan"
    ))

    while True:
        curr = state_mgr.get_current()
        if not curr:
            console.print("[bold red]Kitap kalmadı![/]")
            break

        book = curr["book"]
        chapter = curr["chapter"]

        console.print(CardFormatter.format_card(book, chapter))

        try:
            choice = Prompt.ask(
                f"[bold magenta][{book.id} {chapter.chapter_num}/{book.total_chapters}][/] Sonraki (Enter/n), Önceki (p), Çıkış (q)",
                default="n",
                show_default=False
            ).strip().lower()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Okuma sonlandırıldı. Görüşürüz![/]\n")
            break

        if choice in ["q", "quit", "exit"]:
            console.print("[dim]İlerlemen kaydedildi. İyi günler![/]\n")
            break
        elif choice in ["p", "prev", "previous"]:
            state_mgr.previous()
        else:
            state_mgr.advance()


def cmd_set_book(args):
    loader = BookLoader()
    state_mgr = StateManager(book_loader=loader)
    chapter_num = args.chapter if args.chapter else 1

    success = state_mgr.set_active_book(args.book_id, chapter_num=chapter_num)
    if success:
        console.print(f"[bold green]Aktif kitap güncellendi:[/] '{args.book_id}', Alt Başlık / Bölüm: {chapter_num}")
    else:
        console.print(f"[bold red]Hata:[/] '{args.book_id}' id'li kitap bulunamadı.")


def main():
    parser = argparse.ArgumentParser(description="HoodReads — Kişisel Sokak Kitaplığı Okuyucusu")
    subparsers = parser.add_subparsers(dest="command", help="Komutlar")

    # read / next
    p_read = subparsers.add_parser("read", help="Sıradaki alt başlığı oku ve ilerle")
    subparsers.add_parser("next", help="Sıradaki alt başlığı oku (read ile aynı)")

    # interactive
    subparsers.add_parser("interactive", help="İnteraktif terminal okuyucusunu başlat")

    # list
    subparsers.add_parser("list", help="Kütüphanedeki kitapları ve ilerlemeni gör")

    # preview
    p_preview = subparsers.add_parser("preview", help="Bir kitabın alt başlıklarını önizle")
    p_preview.add_argument("book_id", help="Kitap ID'si (örn: ddia, suc_ve_ceza, donusum, 1984)")
    p_preview.add_argument("--chapter", type=int, default=None, help="Sadece belirli bir ana bölümü göster (örn: --chapter 1)")
    p_preview.add_argument("--limit", type=int, default=None, help="İlk N alt başlığı göster (örn: --limit 5)")

    # set-book
    p_set = subparsers.add_parser("set-book", help="Aktif kitabı ve bölümü ayarla")
    p_set.add_argument("book_id", help="Kitap ID'si")
    p_set.add_argument("--chapter", type=int, default=1, help="Başlanacak alt başlık no (varsayılan: 1)")

    args = parser.parse_args()

    if args.command in ["read", "next"]:
        cmd_read(args)
    elif args.command == "interactive":
        cmd_interactive(args)
    elif args.command == "list":
        cmd_list(args)
    elif args.command == "preview":
        cmd_preview(args)
    elif args.command == "set-book":
        cmd_set_book(args)
    else:
        # Default: if no command passed, show list and offer read
        cmd_list(args)


if __name__ == "__main__":
    main()
