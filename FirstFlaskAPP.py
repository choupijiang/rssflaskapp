from flask import Flask
import feedparser
from flask import render_template
from flask import request
import urllib
import json

app = Flask(__name__)

RSS_FEEDS = {"people": "http://www.people.com.cn/rss/politics.xml",
             "finance": "http://www.people.com.cn/rss/finance.xml",
             }



@app.route("/")
def get_news():
    query = request.args.get("cat")
    if not query or query.lower() not in RSS_FEEDS:
        cat = "people"
    else:
        cat = query.lower()
    feed = feedparser.parse(RSS_FEEDS[cat])
    weather = get_weather("北京")
    return render_template("home.html", weather=weather, articles=feed["entries"])
        

def get_weather(city):
    api_url = "https://www.sojson.com/open/api/weather/json.shtml?city={}".format(city)
    print(api_url)
    url = urllib.parse.quote(api_url)
    data = urllib.request.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {"description": parsed["data"]["quality"], "temperature": parsed["data"]["wendu"], "city": parsed["city"]}
    return weather

if __name__ == '__main__':
    app.run(port=8088, debug=True)
