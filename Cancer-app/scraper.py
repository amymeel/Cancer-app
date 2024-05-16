import feedparser
import json

# URL des flux RSS
RSS_FEED_URL_NEWS = "https://www.iarc.who.int/feed/?post_type=news-events"
RSS_FEED_URL_PRESS = "https://www.iarc.who.int/feed/?post_type=pressrelease"

# Parser flux RSSs
def parse_rss_feed(url):
    return feedparser.parse(url)

# Extraire informations des articles
def print_feed_info(feed):
    for entry in feed.entries:
        print("Title:", entry.title)
        print("Link:", entry.link)
        print("Publication Date:", entry.published)
        print("Author:", entry.author if 'author' in entry else 'No author')
        print("Summary:", entry.summary)
        print("image_url", entry.get('image_url', None))
        print("-" * 50)

# Parser flux RSS news
feed_news = parse_rss_feed(RSS_FEED_URL_NEWS)
print("News:")
print_feed_info(feed_news)

# Parser flux RSS press
feed_press = parse_rss_feed(RSS_FEED_URL_PRESS)
print("Press Releases:")
print_feed_info(feed_press)


# Fonction pour sauvegarder les données dans un fichier JSON
def save_to_json(entries, filename='rss_data.json'):
    with open(filename, 'w') as f:
        json.dump([entry for entry in entries], f)

# Sauvegarder les données dans un fichier JSON pour les news
save_to_json(feed_news.entries, filename='rss_data_news.json')
print("Data for News saved to rss_data_news.json")

# Sauvegarder les données dans un fichier JSON pour la press
save_to_json(feed_press.entries, filename='rss_data_press.json')
print("Data for Press Releases saved to rss_data_press.json")
