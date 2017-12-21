from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import urllib.request
from bs4 import BeautifulSoup
import re


app = Flask(__name__)
ask = Ask(app, "/handelblatt")


def get_headlines():
    url ='http://www.handelsblatt.com/contentexport/feed/schlagzeilen'
    html = urllib.request.urlopen(url).read()
    data = BeautifulSoup(html, 'html.parser')
    headlines = data.find_all('title', limit=7)
    del headlines[0:2]
    description = data.find_all('description', limit=7)
    del description[0:1]
    news = [j for i in zip(headlines, description) for j in i]
    return news

data = get_headlines()
print(data)

"""Titel
 <title>Regierungsbildung: S\xc3\xb6der in 13-k\xc3\xb6pfiger CSU-Delegation f\xc3\xbcr Berliner Sondierungen</title>\n
Erläuternung
<description>Die Entscheidung naht: Am heutigen Donnerstag finden in Katalonien die Parlamentswahlen statt. Die Anleger rechnen mit einer Niederlage der Separatisten und decken sich deshalb mit spanischen Staatsanleihen ein.</description>\n
"""


"""
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


@ask.intend("NoIntent")
def no_intent():
    bye_text = "Na gut, dann halt nicht!"
    return statement(bye_text)


if __name__ == '__main__':
    app.run(debug=True)

"""
