import dash
from dash import dcc, html
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc
import json
from wordcloud import WordCloud
import base64
from datetime import datetime
import gunicorn

# Load JSON data for articles
def load_data(rss_data_news):
    with open(rss_data_news, 'r') as f:
        articles = json.load(f)
    return articles

# Load JSON data for press releases
def load_press_data(rss_data_press):
    with open(rss_data_press, 'r') as f:
        press_releases = json.load(f)
    return press_releases

# Cards for each article
def create_article_cards(articles):
    today = datetime.now().date()
    today_articles = []
    previous_articles = []
    for article in articles:
        article_date = datetime.strptime(article.get('published', ''), '%a, %d %b %Y %H:%M:%S +0000').date()
        if article_date == today:
            today_articles.append(article)
        else:
            previous_articles.append(article)

    today_cards = [dbc.Col(create_card(article), width=6, className="d-flex align-items-stretch") for article in today_articles]
    previous_cards = [dbc.Col(create_card(article), width=6, className="d-flex align-items-stretch") for article in previous_articles]

    return today_cards, previous_cards

# Cards for each press release
def create_press_cards(press_releases):
    today = datetime.now().date()
    today_press_releases = []
    previous_press_releases = []
    for press_release in press_releases:
        press_release_date = datetime.strptime(press_release.get('published', ''), '%a, %d %b %Y %H:%M:%S +0000').date()
        if press_release_date == today:
            today_press_releases.append(press_release)
        else:
            previous_press_releases.append(press_release)

    today_cards = [dbc.Col(create_card(press_release), width=6, className="d-flex align-items-stretch") for press_release in today_press_releases]
    previous_cards = [dbc.Col(create_card(press_release), width=6, className="d-flex align-items-stretch") for press_release in previous_press_releases]

    return today_cards, previous_cards

# Card for an article/press release
def create_card(item):
    card = dbc.Card(
        dbc.CardBody(
            [
                html.A(
                    [
                        html.H4(item.get('title', ''), className="card-title", style={"color": "black", "font-weight": "bold"}),
                        html.P(item.get('summary', ''), className="card-text"),
                        html.Small(item.get('published', ''), className="card-text text-muted"),
                    ],
                    href=item.get('link', ''),
                    target='_blank',
                    style={"text-decoration": "none"}
                ),
            ],
            className="d-flex flex-column"
        ),
        className="mb-4 h-100",
        style={"min-height": "200px"}  # Ensure all cards have the same height
    )
    return card

# Load JSON data from RSS for the word cloud
def load_wordcloud_data(rss_data_news):
    with open(rss_data_news, 'r') as f:
        data_news = json.load(f)
    summaries = [item['summary'] for item in data_news]
    all_summaries = ' '.join(summaries)
    return all_summaries

# Generate the word cloud
def generate_wordcloud(all_summaries):
    wordcloud = WordCloud(width=800, height=600, background_color='white').generate(all_summaries)
    return html.Img(src=wordcloud.to_image(), style={"width": "70%", "margin": "auto", "display": "block"})
###################################
# Create the Dash application
###################################
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])
server = app.server

# Load data for articles, press releases, and word cloud
articles = load_data('rss_data_news.json')
press_releases = load_press_data('rss_data_press.json')
wordcloud_data = load_wordcloud_data('rss_data_news.json')

# Create cards for articles, press releases, and word cloud
today_article_cards, previous_article_cards = create_article_cards(articles)
today_press_cards, previous_press_cards = create_press_cards(press_releases)
wordcloud_figure = generate_wordcloud(wordcloud_data)

# Layout for the articles page
articles_page_layout = html.Div([
    html.H2("Latest Articles", className="my-4"),
    html.H4("Articles of Today", className="my-4"),
    dbc.Container(
        dbc.Row(today_article_cards, justify="center"),
        fluid=True,
    ),
    html.H4("Previous Articles", className="my-4"),
    dbc.Container(
        dbc.Row(previous_article_cards, justify="center"),
        fluid=True,
    ),
    html.Div(id='update-time', style={'position': 'absolute', 'top': '10px', 'right': '10px', 'color': '#6c757d'})
])

# Layout for the press releases page
press_page_layout = html.Div([
    html.H2("Latest Press Releases", className="my-4"),
    html.H4("Press Releases of Today", className="my-4"),
    dbc.Container(
        dbc.Row(today_press_cards, justify="center"),
        fluid=True,
    ),
    html.H4("Previous Press Releases", className="my-4"),
    dbc.Container(
        dbc.Row(previous_press_cards, justify="center"),
        fluid=True,
    ),
    html.Div(id='update-time', style={'position': 'absolute', 'bottom': '10px', 'right': '10px', 'color': '#6c757d'})
])

# Layout for the word cloud page
wordcloud_page_layout = html.Div([
    html.H2("Word Cloud", className="my-4"),
    generate_wordcloud(wordcloud_data)
])

# Layout for the application
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Latest Articles", href="/articles")),
            dbc.NavItem(dbc.NavLink("Latest Press Releases", href="/press-releases")),
            dbc.NavItem(dbc.NavLink("Word Cloud", href="/word-cloud")),
        ],
        brand="International Agency for Research On Cancer News & Press",
        brand_href="/",
        color="primary",
        dark=True,
        className="mb-4"
    ),
    html.Div(id='page-content', className="p-4"),
])


# Callback to display the corresponding page based on the URL
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/articles':
        return articles_page_layout
    elif pathname == '/press-releases':
        return press_page_layout
    elif pathname == '/word-cloud':
        return wordcloud_page_layout
    else:
        return articles_page_layout

# Run the Dash application
if __name__ == '__main__':
    app.run_server(debug=True)