"""Not enough tests here, but it's a good place to start."""
import os

import pytest
import tweepy
from discord_twitter_webhooks import __version__
from discord_twitter_webhooks.main import (
    change_reddit_username_to_link,
    change_subreddit_to_clickable_link,
    get_media_links_and_remove_url,
    get_meta_image,
    get_text,
    remove_utm_source,
    replace_hashtag_with_link,
    replace_tco_url_link_with_real_link,
    replace_username_with_link,
    send_embed_webhook,
    send_text_webhook,
)
from discord_twitter_webhooks.settings import auth

# TODO: Add check for if retweet/reply check is working
# TODO: Add check if imports work, e.g user_list_replies_to_other_tweet_split exists


class TestTweets:
    """Test tweet stuff"""

    api = tweepy.API(auth)
    # https://twitter.com/Bot2Lovi/status/1416158460186611715
    short_tweet_only_text = api.get_status(1416158460186611715)

    # https://twitter.com/Bot2Lovi/status/1416162001076764675
    short_tweet_one_image = api.get_status(1416162001076764675)

    # https://twitter.com/Bot2Lovi/status/1416162224142487555
    short_tweet_two_images = api.get_status(1416162224142487555)

    # https://twitter.com/Bot2Lovi/status/1416162639269539847
    short_tweet_three_images = api.get_status(1416162639269539847)

    # https://twitter.com/Bot2Lovi/status/1416162799777157120
    short_tweet_four_image = api.get_status(1416162799777157120)

    # https://twitter.com/Bot2Lovi/status/1416165082304860160
    long_tweet_only_text = api.get_status(1416165082304860160)

    # https://twitter.com/Bot2Lovi/status/1416193952751947779
    long_tweet_one_image = api.get_status(1416193952751947779)

    # https://twitter.com/Bot2Lovi/status/1416194017197428737
    long_tweet_two_images = api.get_status(1416194017197428737)

    # https://twitter.com/Bot2Lovi/status/1416194068472901634
    long_tweet_three_images = api.get_status(1416194068472901634)

    # https://twitter.com/Bot2Lovi/status/1416194128556199947
    long_tweet_four_image = api.get_status(1416194128556199947)

    # https://twitter.com/Bot2Lovi/status/1416199887293665284
    gif_tweet = api.get_status(1416199887293665284)

    # https://twitter.com/Bot2Lovi/status/1416204465049411593
    at_hash_reddituser_subreddit = api.get_status(1416204465049411593)

    # https://twitter.com/Bot2Lovi/status/1416485664078581761
    retweet_from_somebody_else = api.get_status(1416485664078581761)

    # https://twitter.com/Bot2Lovi/status/1456124564698710017
    link_to_youtube = api.get_status(1456124564698710017)

    webhook_url = os.environ["TEST_WEBHOOK"]

    def test_version(self):
        """Test if the version is correct"""
        assert __version__ == "0.1.0"

    def test_send_text_webhook(self):
        """Test if the text webhook is sent correctly"""
        try:
            send_text_webhook("Running pytest!", webhook=self.webhook_url)
        except Exception as exception:  # pylint: disable=broad-except
            pytest.fail(exception, pytrace=True)

    def test_send_embed_webhook_one_image(self):
        """Test if the embed webhook is sent correctly"""
        try:
            send_embed_webhook(
                tweet=self.short_tweet_one_image,
                webhook=self.webhook_url,
                link_list=["https://pbs.twimg.com/media/E6c309BWYAceCII.jpg"],
                text="Testing embed with one image!",
            )
        except Exception as exception:  # pylint: disable=broad-except
            pytest.fail(exception, pytrace=True)

    def test_send_embed_webhook_four_images(self):
        """Test if the embed webhook is sent correctly"""
        try:
            send_embed_webhook(
                tweet=self.short_tweet_four_image,
                webhook=self.webhook_url,
                link_list=[
                    "https://pbs.twimg.com/media/E6c4jCOXoAIgLW9.jpg",
                    "https://pbs.twimg.com/media/E6c4jCQXoAInLOD.jpg",
                    "https://pbs.twimg.com/media/E6c4jCNXsAAsiYY.jpg",
                    "https://pbs.twimg.com/media/E6c4jCyXMAA4_I9.jpg",
                ],
                text="Testing embed with four images!",
            )
        except Exception as exception:  # pylint: disable=broad-except
            pytest.fail(exception, pytrace=True)

    def test_get_text(self):
        """Test if the text is returned correctly"""
        assert get_text(self.short_tweet_only_text) == "Hello I am short Sadge"
        assert get_text(self.short_tweet_one_image) == "Short 1 Image https://t.co/18WctMxOYa"
        assert get_text(self.short_tweet_two_images) == "Short 2 Images https://t.co/SPBV5a6YyA"
        assert get_text(self.short_tweet_three_images) == "Short 3 Images https://t.co/dWPPTQWbHB"
        assert get_text(self.short_tweet_four_image) == "Short 4 Images https://t.co/OGwDRJCMJF"

        assert get_text(self.retweet_from_somebody_else) == "RT @Bot2Lovi: f saf sasaf sa"

        # TODO: This is not the full text.
        assert (
            get_text(self.long_tweet_only_text)
            == "Hello I am longlanglonglonglonglonglonglonglonglonglonglonglonglonglonglonglong"
            + "longlonglonglonglonglonglonglonglong… https://t.co/WuuOFm4xMk"
        )
        assert (
            get_text(self.long_tweet_one_image)
            == "Long 1 Image Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod "
            + "tempor incididunt ut labore et… https://t.co/2uafrdmqgg"
        )
        assert (
            get_text(self.long_tweet_two_images)
            == "Long 2 Image Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod "
            + "tempor incididunt ut labore et… https://t.co/DH28OdNtsx"
        )
        assert (
            get_text(self.long_tweet_three_images)
            == "Long 3 Image Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod "
            + "tempor incididunt ut labore et… https://t.co/b1a55tQWAZ"
        )
        assert (
            get_text(self.long_tweet_four_image)
            == "Long 4 Image Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod "
            + "tempor incididunt ut labore et… https://t.co/ehh3OWHbqd"
        )

    def test_get_media_links_and_remove_url(self):
        """Test if the media links are returned correctly"""
        short_txt = "Hello I am short Sadge"
        short_1_txt = "Short 1 Image"
        short_2_txt = "Short 2 Images"
        short_3_txt = "Short 3 Images"
        short_4_txt = "Short 4 Images"

        gif_tweet_txt = "Gif"

        assert get_media_links_and_remove_url(tweet=self.short_tweet_only_text, text=short_txt) == ([], short_txt)
        assert get_media_links_and_remove_url(tweet=self.short_tweet_one_image, text=short_1_txt) == (
            [
                "https://pbs.twimg.com/media/E6c309BWYAceCII.jpg",
            ],
            short_1_txt,
        )
        assert get_media_links_and_remove_url(tweet=self.short_tweet_two_images, text=short_2_txt) == (
            [
                "https://pbs.twimg.com/media/E6c4BpyXIAIvvdW.jpg",
                "https://pbs.twimg.com/media/E6c4BqSXMAQq1Fe.jpg",
            ],
            short_2_txt,
        )
        assert get_media_links_and_remove_url(tweet=self.short_tweet_three_images, text=short_3_txt) == (
            [
                "https://pbs.twimg.com/media/E6c4Zw0WQAQHA6h.jpg",
                "https://pbs.twimg.com/media/E6c4Zw-WUAIr0pJ.jpg",
                "https://pbs.twimg.com/media/E6c4Zx4WUAALtpv.jpg",
            ],
            short_3_txt,
        )
        assert get_media_links_and_remove_url(tweet=self.short_tweet_four_image, text=short_4_txt) == (
            [
                "https://pbs.twimg.com/media/E6c4jCOXoAIgLW9.jpg",
                "https://pbs.twimg.com/media/E6c4jCQXoAInLOD.jpg",
                "https://pbs.twimg.com/media/E6c4jCNXsAAsiYY.jpg",
                "https://pbs.twimg.com/media/E6c4jCyXMAA4_I9.jpg",
            ],
            short_4_txt,
        )

        assert get_media_links_and_remove_url(tweet=self.gif_tweet, text=gif_tweet_txt) == (
            [
                "https://pbs.twimg.com/tweet_video_thumb/E6daSHUX0AYR9ap.jpg",
            ],
            gif_tweet_txt,
        )

    def test_replace_username_with_link(self):
        """Test if the username is replaced with a link"""
        assert (
            replace_username_with_link(self.at_hash_reddituser_subreddit.text)
            == "Hello [@TheLovinator1](https://twitter.com/TheLovinator1) #Hello /u/test /r/aww"
        )

    def test_replace_hashtag_with_link(self):
        """Test if the hashtag is replaced with a link"""
        assert (
            replace_hashtag_with_link(self.at_hash_reddituser_subreddit.text)
            == "Hello @TheLovinator1 [#Hello](https://twitter.com/hashtag/Hello) /u/test /r/aww"
        )

    def test_change_subreddit_to_clickable_link(self):
        """Test if the subreddit is replaced with a clickable link"""
        assert (
            change_subreddit_to_clickable_link(self.at_hash_reddituser_subreddit.text)
            == "Hello @TheLovinator1 #Hello /u/test [/r/aww](https://reddit.com/r/aww)"
        )

    def test_change_reddit_username_to_link(self):
        """Test if the reddit username is replaced with a link"""
        assert (
            change_reddit_username_to_link(self.at_hash_reddituser_subreddit.text)
            == "Hello @TheLovinator1 #Hello [/u/test](https://reddit.com/u/test) /r/aww"
        )

    def test_get_meta_image(self):
        """Test if the meta image is returned correctly"""
        assert get_meta_image("https://lovinator.space/") == "https://lovinator.space/KaoFace.webp"

    def test_replace_tco_url_link_with_real_link(self):
        """Test if the tco url is replaced with the real link"""
        assert (
            replace_tco_url_link_with_real_link(self.short_tweet_only_text, self.short_tweet_only_text.text)
            == "Hello I am short Sadge"
        )
        assert (
            replace_tco_url_link_with_real_link(tweet=self.link_to_youtube, text=self.link_to_youtube.text)
            == "https://www.youtube.com/\nHello, this is Youtube"
        )

    def test_remove_utm_source(self):
        """Test if the utm source is removed"""
        assert (
            remove_utm_source(
                "https://store.steampowered.com/app/457140/Oxygen_Not_Included/?utm_source=Steam&utm_campaign=Sale&utm_medium=Twitter"
            )
            == "https://store.steampowered.com/app/457140/Oxygen_Not_Included/"
        )