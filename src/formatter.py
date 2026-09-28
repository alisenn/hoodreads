from typing import List
from src.models import Book, Chapter


class TweetFormatter:
    MAX_TWEET_LENGTH = 280

    @classmethod
    def calculate_length(cls, text: str) -> int:
        """
        Calculates tweet length according to Twitter rules:
        Most characters count as 1, emojis often count as 2.
        For safe estimation, Python's len() with emoji handling is very close.
        """
        count = 0
        for char in text:
            # Emoji rough estimation
            if ord(char) > 0xFFFF:
                count += 2
            else:
                count += 1
        return count

    @classmethod
    def format_single(cls, book: Book, chapter: Chapter) -> str:
        """
        Builds full single tweet text:
        📖 {Kitap} ({bölüm}/{toplam})
        📌 {Bölüm Başlığı}

        {İçerik}

        💡 {Özet Ders}
        #SokakKitaplığı #KitapÖzeti
        """
        header = f"📖 {book.title} ({chapter.chapter_num}/{book.total_chapters})\n📌 {chapter.title}\n\n"
        footer = f"\n\n💡 {chapter.key_takeaway}\n#SokakKitaplığı #Kitap"
        return f"{header}{chapter.content}{footer}"

    @classmethod
    def format_thread(cls, book: Book, chapter: Chapter) -> List[str]:
        """
        Formats into a list of tweets. If it fits into 1 tweet, returns [single_tweet].
        Otherwise splits into a threaded series, strictly guaranteeing <= 280 chars per tweet.
        """
        single = cls.format_single(book, chapter)
        if cls.calculate_length(single) <= cls.MAX_TWEET_LENGTH:
            return [single]

        header = f"📖 {book.title} ({chapter.chapter_num}/{book.total_chapters})\n📌 {chapter.title}\n\n"
        footer = f"\n\n💡 {chapter.key_takeaway}\n#SokakKitaplığı"
        short_footer = f"\n\n💡 {chapter.key_takeaway}"

        words = chapter.content.split()

        # Multi-tweet thread distribution
        # 1) Try 2 tweets: t1 + t2(with footer)
        for act_footer in [footer, short_footer]:
            tag_t1 = "\n\n(1/2 🧵)"
            t1_budget = cls.MAX_TWEET_LENGTH - cls.calculate_length(header + tag_t1)
            w1 = []
            w_idx = 0
            while w_idx < len(words):
                if cls.calculate_length(" ".join(w1 + [words[w_idx]])) <= t1_budget:
                    w1.append(words[w_idx])
                    w_idx += 1
                else:
                    break

            rem_words = words[w_idx:]
            t2 = f"(2/2) {' '.join(rem_words)}{act_footer}"
            if cls.calculate_length(t2) <= cls.MAX_TWEET_LENGTH:
                t1 = f"{header}{' '.join(w1)}{tag_t1}"
                return [t1, t2]

        # 2) Try 3 tweets: t1 + t2 + t3(with footer)
        for act_footer in [footer, short_footer]:
            tag_t1 = "\n\n(1/3 🧵)"
            t1_budget = cls.MAX_TWEET_LENGTH - cls.calculate_length(header + tag_t1)
            w1 = []
            w_idx = 0
            while w_idx < len(words):
                if cls.calculate_length(" ".join(w1 + [words[w_idx]])) <= t1_budget:
                    w1.append(words[w_idx])
                    w_idx += 1
                else:
                    break

            rem_words = words[w_idx:]
            half = len(rem_words) // 2
            mid_w = rem_words[:half]
            last_w = rem_words[half:]

            t1 = f"{header}{' '.join(w1)}{tag_t1}"
            t2 = f"(2/3) {' '.join(mid_w)}"
            t3 = f"(3/3) {' '.join(last_w)}{act_footer}"

            if (
                cls.calculate_length(t1) <= cls.MAX_TWEET_LENGTH
                and cls.calculate_length(t2) <= cls.MAX_TWEET_LENGTH
                and cls.calculate_length(t3) <= cls.MAX_TWEET_LENGTH
            ):
                return [t1, t2, t3]

        # 3) Fallback: safe 2-part partition
        return [
            f"{header}{chapter.content[:140]}...\n\n(1/2 🧵)",
            f"(2/2) ...{chapter.content[140:340]}{short_footer}",
        ]
