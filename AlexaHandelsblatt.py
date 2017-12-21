from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import urllib.request
from bs4 import BeautifulSoup


app = Flask(__name__)
ask = Ask(app, "/")


def get_headlines():
    url ='http://www.handelsblatt.com/contentexport/feed/schlagzeilen'
    html = urllib.request.urlopen(url).read()
    data = BeautifulSoup(html, 'html.parser')
    headlines = data.find_all('title', limit=7)
    del headlines[0:2]
    description = data.find_all('description', limit=7)
    del description[0:1]
    news = [j for i in zip(headlines, description) for j in i]
    news = '...'.join(str(x) for x in news)
    news = news.replace("<title>", "")
    news = news.replace("</title>", "")
    news = news.replace("<description>", "")
    news = news.replace("</description>", "")


    return news


@app.route('/')
def homepage():
    return "hi there"


@ask.launch
def start_skill():
    welcome_msg = "Guten Tag, möchten Sie die Handelsblatt News hören?"
    return question(welcome_msg)


@ask.intent("YesIntent")
def share_headlines():
    headlines = get_headlines()
    headline_msg = 'Die derzeitigen Nachrichten auf Handelsblatt{}'.format(headlines)
    return statement(headline_msg)


@ask.intent"NoIntent")
def no_intent():
    bye_text = "Na gut, dann halt nicht!"
    return statement(bye_text)


if __name__ == '__main__':
    app.run(debug=True)


