import os
import re

import pymongo
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from Parser.Parser.settings import MONGO_URI, MONGO_DATABASE, MONGO_COLLECTION_NAME
from WebApp.tables import ArticlesTable, CommentsTable
from flask_pymongo import PyMongo
from collections import Counter

app = Flask(__name__, template_folder='templates')
Bootstrap(app)
app.config["MONGO_URI"] = f"{MONGO_URI}{MONGO_DATABASE}"
mongo = PyMongo(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form['number'].isdigit():
            refresh(int(request.form['number']))
    records = mongo.db.idnes.find({})
    return render_template('index.html', articles_table=ArticlesTable(records))


@app.route('/detail/<int:id>')
def detail(id):
    record = mongo.db.idnes.find_one({'id':id})
    return render_template('details.html', record=record, CommentsTable=CommentsTable)


@app.route('/filters', methods=['GET', 'POST'])
def filters():
    if request.method == 'POST':
        if request.form['number'].isdigit() and request.form['filters'] == 'Most common words':
            records = mongo.db.idnes.find({})
            data_set = []
            for record in records:
                data_set.extend(normalize_str_to_list(record['header']))
                data_set.extend(normalize_str_to_list(record['opener']))
                data_set.extend(split_paragraphs_into_words(record['paragraphs']))
                data_set.extend(split_comments_into_words(record['comments']))

            counter = Counter(data_set)
            most_common = counter.most_common(n=int(request.form['number']))
            return render_template('filters.html', most_common_words=most_common)

        if request.form['number'].isdigit() and request.form['filters'] == 'Most commented':
            records = list(mongo.db.idnes.find({}))
            records.sort(reverse=True, key=lambda record: len(record['comments']))

            return render_template('filters.html', most_commented=records,
                                   number_of_results=int(request.form['number']), len=len, enumerate=enumerate)

    return render_template('filters.html')


def refresh(number_of_items:int = 10):
    os.system(f'cd ../Parser && python run.py {number_of_items}')


def split_paragraphs_into_words(paragraphs):
    final_list = []
    list_of_lists_of_words = [normalize_str_to_list(paragraph) for paragraph in paragraphs]
    for list_of_words in list_of_lists_of_words:
        final_list.extend(list_of_words)
    return final_list

def split_comments_into_words(comments):
    final_list = []
    for comment in comments:
        final_list.extend(normalize_str_to_list(comment['text']))
    return final_list

def normalize_str_to_list(word:str):
    return word.replace('.', '').replace(',', '').replace('?', '').lower().split()
