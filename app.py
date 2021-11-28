from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os
import string
import random

app = Flask(__name__)

# Configuring SQLite Database

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class GetURL(db.Model):

    __tablename__ = 'url_shortener'

    id = db.Column(db.Integer, primary_key=True)
    org_url = db.Column(db.Text)
    short_url = db.Column(db.Text)



    def __init__(self, org_url, short_url):

        self.org_url = org_url
        self.short_url = short_url

    def __repr__(self):
        return f"{self.org_url} ---> {self.short_url}"

def init_db():
    db.create_all()

data = {}

@app.route('/')
def home_getURI():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def home_postURI():
    added_num_str = 7
    original_url = request.form.get('url_in')
    short_url = ''.join(random.choices(string.ascii_letters + string.digits, k=added_num_str))
    data[short_url] = original_url
    new_data = GetURL(original_url, short_url)
    db.session.add(new_data)
    db.session.commit()
    return render_template('index.html', k = short_url)


@app.route('/generated-links')
def links():
    urls = GetURL.query.all()
    return render_template('links.html', data = data, urls = urls)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/srse/<short_url>')
def open_listed_url(short_url):
    if (short_url) in data:
        return redirect(data[(short_url)])
    return "incorrect URL"

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
