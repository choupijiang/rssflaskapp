from flask import Flask
import feedparser
from flask import render_template
from flask import request


app = Flask(__name__)

RSS_FEEDS = {"people": "http://www.people.com.cn/rss/politics.xml",
             "finance": "http://www.people.com.cn/rss/finance.xml",
             }



# @app.route('/')
# def hello_world():
#     return 'Hello World!'

# @app.route('/')
# @app.route('/people')
# def get_people():
#     return get_news("people")
#
# @app.route("/finance")
# def get_finance():
#     return get_news("finance")


# @app.route("/")
# @app.route("/<cat>")
# def get_news(cat="people"):
#     feed = feedparser.parse(RSS_FEEDS[cat])
#     first_artical = feed["entries"][0]
#     return """<html>
#         <body>
#             <h1>pepple</h1>
#             <b>{0}</b><br>
#             <i>{1}</i><br>
#             <p>{2}</p><br>
#         </body>
#     </html>
#     """.format(first_artical.get("title"), first_artical.get("published"), first_artical.get("summary"))

# @app.route("/")
# @app.route("/<cat>")
# def get_news(cat="people"):
#     feed = feedparser.parse(RSS_FEEDS[cat])
#     first_artical = feed["entries"][0]
#     return render_template("home.html",
#                 title=first_artical.get("title"),
#                 published=first_artical.get("published"),
#                 summary=first_artical.get("summary")
#             )

# @app.route("/")
# @app.route("/<cat>")
# def get_news(cat="people"):
#     feed = feedparser.parse(RSS_FEEDS[cat])
#     first_artical = feed["entries"][0]
#     return render_template("home.html", article=first_artical)
   
# @app.route("/")
# @app.route("/<string:cat>/")
# def get_news(cat="people"):
#     feed = feedparser.parse(RSS_FEEDS[cat])
#     articles = feed["entries"]
#     return render_template("home.html", articles=articles)


@app.route("/")
def get_news():
    query = request.args.get("cat")
    if not query or query.lower() not in RSS_FEEDS:
        cat = "people"
    else:
        cat = query.lower()
    feed = feedparser.parse(RSS_FEEDS[cat])
    return render_template("home.html", articles=feed["entries"])
        

if __name__ == '__main__':
    app.run(port=8088, debug=True)
