from typing import TYPE_CHECKING

from flask import Flask, request

from discord_twitter_webhooks.settings import init_reader

if TYPE_CHECKING:
    from reader import Feed

app = Flask(__name__)


@app.route("/")
def index() -> str:
    html: str = ""
    html += "<h1>Discord Twitter Webhooks</h1>"
    reader = init_reader()

    if reader is None:
        return "Failed to initialize reader"

    reader.update_feeds()

    html_before = html

    for feed in reader.get_feeds():
        html += f"<h2>{feed.url}</h2>"

    if html == html_before:
        html += "<p>You can add more feeds here: <a href='/add'>/add</a></p>"

    return html


@app.route("/add")
def add() -> str:
    html: str = ""
    html += "<h1>Add a feed</h1>"
    html += "<style>body { background-color: #111111; color: #DCDDDE; }</style>"
    html += (
        "<script> function validateForm() { var x = document.forms['add']['name'].value; if (x == '') { alert('Name"
        " must be filled out'); return false; } var x = document.forms['add']['usernames'].value; if (x == '') {"
        " alert('Usernames must be filled out'); return false; } var x = document.forms['add']['url'].value; if (x =="
        " '') { alert('Webhook URL must be filled out'); return false; } } </script>"
    )
    html += "<form name='add' action='/add' onsubmit='return validateForm()' method='post'>"
    html += "<label for='name'>Name:</label><br>"
    html += "<input type='text' id='name' name='name' value=''><br>"
    html += "<label for='usernames'>Usernames: (separate with spaces)</label><br>"
    html += "<input type='text' id='usernames' name='usernames' value=''><br>"
    html += "<label for='url'>Webhook URL:</label><br>"
    html += "<input type='url' id='url' name='url' value=''><br><br>"
    html += "<input type='checkbox' id='include_retweets' name='include_retweets' value='true'>"
    html += "<label for='include_retweets'>Include retweets</label><br>"
    html += "<input type='checkbox' id='include_replies' name='include_replies' value='true'>"
    html += "<label for='include_replies'>Include replies</label><br>"
    html += "<input type='submit' value='Submit'>"
    html += "</form>"
    return html


@app.route("/add", methods=["POST"])
def add_post() -> str:
    reader = init_reader()

    if reader is None:
        return "Error"

    name: str | None = request.form.get("name")
    webhook_value: str | None = request.form.get("url")
    usernames_value: str | None = request.form.get("usernames")
    include_retweets_value: str | None = request.form.get("include_retweets")
    include_replies_value: str | None = request.form.get("include_replies")

    if webhook_value is None or usernames_value is None:
        return "Error"

    username_list: list[str] = usernames_value.split(" ")

    include_retweets: bool = include_retweets_value == "true"
    include_replies: bool = include_replies_value == "true"

    for username in username_list:
        feed_url: str = f"https://nitter.lovinator.space/{username}/rss"
        reader.add_feed(feed_url, exist_ok=True)

        feed: Feed = reader.get_feed(feed_url)

        # Add webhook, include_retweets and include_replies to the feed as tags
        reader.set_tag(feed, "name", name)  # type: ignore
        reader.set_tag(feed, "webhook", webhook_value or None)  # type: ignore
        reader.set_tag(feed, "include_retweets", include_retweets or False)  # type: ignore
        reader.set_tag(feed, "include_replies", include_replies or False)  # type: ignore

        feed_name: str | None = reader.get_tag(feed, "name")  # type: ignore
        feed_webhook: str | None = reader.get_tag(feed, "webhook")  # type: ignore
        feed_include_retweets: bool | None = reader.get_tag(feed, "include_retweets")  # type: ignore
        feed_include_replies: bool | None = reader.get_tag(feed, "include_replies")  # type: ignore

        if feed_name is None or feed_webhook is None or feed_include_retweets is None or feed_include_replies is None:
            return (
                f"Error - Something was None that shouldn't be it:\nname: {feed_name}\nwebhook: {feed_webhook}\n"
                f"include_retweets: {feed_include_retweets}\ninclude_replies: {feed_include_replies}"
            )
    return f"Added {name} with usernames {usernames_value} and webhook {webhook_value} to the database."
