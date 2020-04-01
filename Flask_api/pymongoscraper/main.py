import pymongo
from flask import *

from .extensions import mongo

from flask import Flask, request, redirect, url_for, make_response


main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    articles = mongo.db.SectorSK_articles
    results_number = 0
    all_results = articles.find().limit(results_number)
    article_set = zipIt(all_results)

    if request.method == 'POST':
        number = request.form['number']
        results_number = int(number)
        option = option = request.form['options']

        if option == "datum":
            results_date = articles.find().limit(results_number).sort('published', pymongo.DESCENDING)
            article_set_date = zipIt(results_date)
            return render_template("results.html", article_set=article_set_date, number=number)

        if option == "koment":
            results_comment = articles.find().limit(results_number).sort('comments_count', pymongo.DESCENDING)
            article_set_comment = zipIt(results_comment)
            return render_template("results.html", article_set=article_set_comment, number=number)

    else:
        return render_template("results.html", article_set=article_set)

def zipIt(mongoCollection):
    titles = []
    authors = []
    urls = []
    published = []
    categories = []
    comments = []
    tags = []
    parags = []
    parag2 = []

    for r in mongoCollection:
        titles.append(r['article_title'])
        authors.append(r['article_author'])
        urls.append(r['article_url'])
        published.append(r['published'])
        categories.append(r['category'])
        comments.append(r['comments_count'])
        parags.append(r['paragraphs'][0])
        parag2.append(r['paragraphs'][1])
        tags.append(r['tags'])

    return zip(titles, authors, urls, published, categories, comments, parags, parag2, tags)




