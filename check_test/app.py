import os
import sqlite3
from flask import Flask, render_template, abort, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
# GETメソッドの場合
@app.route("/test1")
def test1():
    favs = request.args.getlist("fav")
    print("favs:", favs) # ['1','2','3']
    return "ok"

# POSTメソッドの場合
@app.route("/test2", methods=['POST'])
def test2():
    favs = request.form.getlist("fav")
    print("favs:", favs) # ['1','2','3']
    return "ok"

if __name__ == '__main__':
    app.debug = True # デバッグモード有効化
    app.run(host='0.0.0.0') # どこからでもアクセス可能に
