import os
from typing import List, Optional, Tuple
from dotenv import load_dotenv

load_dotenv()

try:
    import tweepy
except ImportError:
    tweepy = None


class TwitterClient:
    def __init__(self, force_dry_run: bool = False):
        self.api_key = os.getenv("TWITTER_API_KEY")
        self.api_secret = os.getenv("TWITTER_API_SECRET")
        self.access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        self.access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
        self.bearer_token = os.getenv("TWITTER_BEARER_TOKEN")

        self.has_credentials = all([
            self.api_key,
            self.api_secret,
            self.access_token,
            self.access_token_secret,
        ]) and "your_" not in (self.api_key or "")

        self.dry_run = force_dry_run or not self.has_credentials
        self.client = None

        if not self.dry_run and tweepy is not None:
            try:
                self.client = tweepy.Client(
                    bearer_token=self.bearer_token,
                    consumer_key=self.api_key,
                    consumer_secret=self.api_secret,
                    access_token=self.access_token,
                    access_token_secret=self.access_token_secret,
                )
            except Exception as e:
                print(f"[!] Tweepy başlatılamadı, DRY-RUN moduna geçiliyor: {e}")
                self.dry_run = True

    def post_tweet(self, text: str, in_reply_to_tweet_id: Optional[str] = None) -> Tuple[bool, Optional[str]]:
        if self.dry_run:
            # Simulated ID
            mock_id = f"sim_{abs(hash(text)) % 100000000}"
            return True, mock_id

        if not self.client:
            return False, "Twitter client yapılandırılmamış."

        try:
            kwargs = {"text": text}
            if in_reply_to_tweet_id:
                kwargs["in_reply_to_tweet_id"] = in_reply_to_tweet_id
            response = self.client.create_tweet(**kwargs)
            tweet_id = str(response.data["id"])
            return True, tweet_id
        except Exception as e:
            return False, str(e)

    def post_thread(self, tweets: List[str]) -> Tuple[bool, List[str], Optional[str]]:
        """
        Posts sequential tweets as a reply chain / thread.
        """
        tweet_ids = []
        last_id = None

        for idx, text in enumerate(tweets):
            success, result = self.post_tweet(text, in_reply_to_tweet_id=last_id)
            if not success:
                return False, tweet_ids, f"Tweet {idx + 1} atılırken hata: {result}"
            last_id = result
            tweet_ids.append(result)

        return True, tweet_ids, None
