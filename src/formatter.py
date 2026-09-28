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
        Otherwise splits sentences into 2 or more threaded tweets, guaranteeing <= 280 chars each.
        """
        single = cls.format_single(book, chapter)
        if cls.calculate_length(single) <= cls.MAX_TWEET_LENGTH:
            return [single]

        # Multi-tweet thread splitting
        header = f"📖 {book.title} ({chapter.chapter_num}/{book.total_chapters})\n📌 {chapter.title}\n\n"
        footer = f"\n\n💡 {chapter.key_takeaway}\n#SokakKitaplığı"
        short_footer = f"\n\n💡 {chapter.key_takeaway}"

        # We want to format across parts (1, 2, or 3)
        # Split content into words or small phrases to safely fit limits
        words = chapter.content.split()
        
        # Test 2 parts, then 3 parts
        for total_parts in [2, 3]:
            tweets = []
            word_idx = 0
            possible = True

            for part_num in range(1, total_parts + 1):
                is_first = (part_num == 1)
                is_last = (part_num == total_parts)

                if is_first:
                    prefix = header
                    suffix = f"\n\n(1/{total_parts} 🧵)"
                elif is_last:
                    prefix = f"({total_parts}/{total_parts}) "
                    suffix = footer
                else:
                    prefix = f"({part_num}/{total_parts}) "
                    suffix = ""

                # Base overhead
                base_len = cls.calculate_length(prefix + suffix)
                available = cls.MAX_TWEET_LENGTH - base_len

                if is_last and available < 60:
                    # Try with shorter footer
                    suffix = short_footer
                    base_len = cls.calculate_length(prefix + suffix)
                    available = cls.MAX_TWEET_LENGTH - base_len

                part_words = []
                if is_last:
                    # Last part takes all remaining words
                    part_words = words[word_idx:]
                    content_str = " ".join(part_words)
                    tweet_str = f"{prefix}{content_str}{suffix}"
                    if cls.calculate_length(tweet_str) <= cls.MAX_TWEET_LENGTH:
                        tweets.append(tweet_str)
                    else:
                        # Try without hashtag in footer
                        tweet_str = f"{prefix}{content_str}{short_footer}"
                        if cls.calculate_length(tweet_str) <= cls.MAX_TWEET_LENGTH:
                            tweets.append(tweet_str)
                        else:
                            possible = False
                    break
                else:
                    while word_idx < len(words):
                        test_words = part_words + [words[word_idx]]
                        if cls.calculate_length(" ".join(test_words)) <= available:
                            part_words.append(words[word_idx])
                            word_idx += 1
                        else:
                            break

                    if not part_words or word_idx >= len(words):
                        possible = False
                        break

                    tweets.append(f"{prefix}{' '.join(part_words)}{suffix}")

            if possible and len(tweets) == total_parts:
                return tweets

        # Fallback safe partition
        part1_max = cls.MAX_TWEET_LENGTH - cls.calculate_length(header + "\n\n(1/2 🧵)")
        w1 = []
        w_idx = 0
        while w_idx < len(words) and cls.calculate_length(" ".join(w1 + [words[w_idx]])) <= part1_max:
            w1.append(words[w_idx])
            w_idx += 1
        
        t1 = f"{header}{' '.join(w1)}\n\n(1/2 🧵)"
        t2_body = " ".join(words[w_idx:])
        t2 = f"(2/2) {t2_body}{short_footer}"
        return [t1, t2]
