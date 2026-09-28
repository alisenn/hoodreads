import argparse
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from src.book_loader import BookLoader
from src.state_manager import StateManager
from src.formatter import TweetFormatter
from src.twitter_client import TwitterClient

console = Console()


def cmd_list(args):
    loader = BookLoader()
    books = loader.load_all_books()
    state_mgr = StateManager(book_loader=loader)
    state = state_mgr.load_state()

    active_id = state.get("current_book_id")
    curr_chapter = state.get("current_chapter_num", 1)

    table = Table(title="📚 Sokak Kitaplığı — Mevcut Kitaplar", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="cyan", width=15)
    table.add_column("Kitap Adı", style="bold green", width=22)
    table.add_column("Yazar", style="yellow", width=20)
    table.add_column("Bölüm", justify="center", width=8)
    table.add_column("Durum", style="bold", width=18)

    for b_id, book in books.items():
        if b_id == active_id:
            status = f"[bold green]▶ Aktif ({curr_chapter}/{book.total_chapters})[/]"
        else:
            status = "[dim]Beklemede[/]"
        table.add_row(book.id, book.title, book.author, str(book.total_chapters), status)

    console.print(table)
    console.print("\n[dim]İpucu: Bir kitabı seçmek için: python main.py set-book <kitap_id>[/]\n")


def cmd_preview(args):
    loader = BookLoader()
    book = loader.get_book(args.book_id)
    if not book:
        console.print(f"[bold red]Hata:[/] '{args.book_id}' id'li kitap bulunamadı.")
        return

    console.print(Panel(f"[bold yellow]{book.title}[/] - {book.author}\n[italic]{book.tagline}[/]", title="📖 Kitap Detayı", border_style="cyan"))

    for ch in book.chapters:
        tweets = TweetFormatter.format_thread(book, ch)
        for idx, t in enumerate(tweets):
            len_info = f"({TweetFormatter.calculate_length(t)}/280 kar.)"
            console.print(Panel(t, title=f"Bölüm {ch.chapter_num} (Tweet {idx + 1}/{len(tweets)}) {len_info}", border_style="green"))


def cmd_tweet(args):
    loader = BookLoader()
    state_mgr = StateManager(book_loader=loader)
    task = state_mgr.get_next_task()

    if not task:
        console.print("[bold red]Hata:[/] Yayınlanacak bölüm bulunamadı. Kütüphanede kitap var mı?")
        return

    book = task["book"]
    chapter = task["chapter"]
    tweets = TweetFormatter.format_thread(book, chapter)

    force_dry_run = not args.live
    client = TwitterClient(force_dry_run=force_dry_run)

    mode_label = "[bold yellow]DRY-RUN (Simülasyon)[/]" if client.dry_run else "[bold green]CANLI TWITTER (X)[/]"
    console.print(f"\n🚀 Mod: {mode_label}")
    console.print(f"📖 Kitap: [bold cyan]{book.title}[/] | Bölüm: [bold yellow]{chapter.chapter_num}/{book.total_chapters}[/]\n")

    for i, t in enumerate(tweets):
        char_count = TweetFormatter.calculate_length(t)
        badge = "[green]✓ Uygun[/]" if char_count <= 280 else "[red]✗ Limit Aşımı[/]"
        console.print(Panel(t, title=f"Tweet {i + 1}/{len(tweets)} — {char_count}/280 {badge}", border_style="blue"))

    success, tweet_ids, error = client.post_thread(tweets)
    if success:
        console.print(f"\n[bold green]✅ Başarıyla yayınlandı / simüle edildi![/] Tweet ID'leri: {tweet_ids}")
        state_mgr.advance(tweet_id=tweet_ids[0] if tweet_ids else None)
        next_task = state_mgr.get_next_task()
        if next_task:
            console.print(f"[dim]Sıradaki hedef: {next_task['book'].title} - Bölüm {next_task['chapter'].chapter_num}[/]\n")
    else:
        console.print(f"\n[bold red]❌ Tweet atılırken hata oluştu:[/] {error}\n")


def cmd_set_book(args):
    loader = BookLoader()
    state_mgr = StateManager(book_loader=loader)
    chapter_num = args.chapter if args.chapter else 1

    success = state_mgr.set_active_book(args.book_id, chapter_num=chapter_num)
    if success:
        console.print(f"[bold green]Aktif kitap güncellendi:[/] '{args.book_id}', Bölüm: {chapter_num}")
    else:
        console.print(f"[bold red]Hata:[/] '{args.book_id}' id'li kitap bulunamadı.")


def main():
    parser = argparse.ArgumentParser(description="Sokak Ağzıyla Kitap Özeti Twitter Botu")
    subparsers = parser.add_subparsers(dest="command", help="Komutlar")

    # list
    subparsers.add_parser("list", help="Kütüphanedeki kitapları listele")

    # preview
    p_preview = subparsers.add_parser("preview", help="Bir kitabın tüm sokak özetlerini gör")
    p_preview.add_argument("book_id", help="Kitap ID'si (örn: suc_ve_ceza, donusum, 1984)")

    # tweet
    p_tweet = subparsers.add_parser("tweet", help="Sıradaki bölümü tweetle")
    p_tweet.add_argument("--live", action="store_true", help="Gerçek Twitter hesabına at (varsayılan: simülasyon)")

    # set-book
    p_set = subparsers.add_parser("set-book", help="Aktif kitabı ve bölümü ayarla")
    p_set.add_argument("book_id", help="Kitap ID'si")
    p_set.add_argument("--chapter", type=int, default=1, help="Başlanacak bölüm (varsayılan: 1)")

    args = parser.parse_args()

    if args.command == "list":
        cmd_list(args)
    elif args.command == "preview":
        cmd_preview(args)
    elif args.command == "tweet":
        cmd_tweet(args)
    elif args.command == "set-book":
        cmd_set_book(args)
    else:
        # Default: show help and list
        parser.print_help()
        console.print("\n")
        cmd_list(args)


if __name__ == "__main__":
    main()
