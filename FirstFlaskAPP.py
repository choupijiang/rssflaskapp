from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
import feedparser
import urllib
import json
import string
import ssl
import datetime

app = Flask(__name__)

RSS_FEEDS = {"people": "http://www.people.com.cn/rss/politics.xml",
             "finance": "http://www.people.com.cn/rss/finance.xml",
             }



@app.route("/")
def home():
    cat = request.args.get("cat")
    if not cat:
        cat = request.cookies.get("cat")
        if not cat:
            cat = "finance"
    articles = get_news(cat)

    context=urllib.request.urlopen( 'http://pv.sohu.com/cityjson').read()
    city=context.decode("gb2312").split("=")[1].split(",")[2].split('"')[3]
    if not city:
        city = "北京"
    weather = get_weather(city)
    response = make_response(render_template("home.html", articles=articles, weather=weather))
    expires = datetime.datetime.now() + datetime.timedelta(days = 1)
    response.set_cookie("cat", cat, expires=expires)
    return response


def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        cat = "people"
    else:
        cat = query.lower()
    feed = feedparser.parse(RSS_FEEDS[cat])
    return feed["entries"]
        

def get_weather(city):
    api_url = "https://www.sojson.com/open/api/weather/json.shtml?city={}".format(city)
    parsed_url = urllib.parse.quote(api_url, safe=string.printable)
    context = ssl._create_unverified_context()
    data = urllib.request.urlopen(parsed_url, context=context)
    parsed = json.loads(data.read())
    weather = None
    if parsed.get("data"):
        weather = {"description": parsed["data"]["quality"], "temperature": parsed["data"]["wendu"], "city": parsed["city"]}
    return weather

if __name__ == '__main__':
    app.run(port=8090, debug=True)
