import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/movie", methods=["POST"])
def movie_post():
    url_recieve = request.form['url_give']
    star_recieve = request.form['star_give']
    comment_recieve = request.form['comment_give']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }
    data = requests.get(url_recieve, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    og_image = soup.select_one('meta[property="og:image"]')
    og_title = soup.select_one('meta[property="og:title"]')
    og_description = soup.select_one('meta[property="twitter:image:alt"]')
    image = og_image['content']
    title = og_title['content']
    description = og_description['content']
    doc = {
        'image' : image,
        'title' : title,
        'description' : description,
        'star' : star_recieve,
        'comment' : comment_recieve
    }
    db.movie.insert_one(doc)
    return jsonify({'msg':'Film berhasil ditambahkan!'})

@app.route("/movie", methods=["GET"])
def movie_get():
    movie_list = list(db.movie.find({},{'_id': False}))
    return jsonify({'movies': movie_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)