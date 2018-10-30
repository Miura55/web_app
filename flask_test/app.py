# coding: utf-8

from flask import Flask, render_template, abort, request
from flaski.models import WikiContent
from flaski.database import db_session
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

# 起動されたサーバーの/にアクセスした時の挙動を記述。
# @app.route("/hoge")で記述すれば、http://127.0.0.1:5000/aaでアクセスした時の挙動を記述できる。
@app.route("/")
def hello():
    contents = WikiContent.query.all()
    # index.htmlにcontensを引数に渡して実行。
    return render_template("index.html", contents=contents)

#/<title>を指定することで、index.htmlのtitle=content.titleを指定している。methods=["GET"]で、GETリクエストを指定。
@app.route("/<title>", methods=["GET"])
def show_content(title):
    """
    :param title:modelに対するクエリ文字列
    :return:
    """
    # wikicontentテーブルから、titleでフィルタ(where指定して取得) firstは1行だけ取得するの意味。
    # all()だと、結果を複数リスト形式で取得する。
    content = WikiContent.query.filter_by(title=title).first()
    if content is None:
        abort(404)
    # show_content.htmlを表示。引数にcontentを渡す。
    return render_template("show_content.html", content=content)

@app.route("/<title>", methods=["POST"])
def post_content(title=None):
    if title is None:
        abort(404)
    content = WikiContent.query.filter_by(title=title).first()
    # contentが取得できていなければinsertするため、WikiContentのインスタンスを生成
    if content is None:
        content = WikiContent(title,
                              request.form["body"]
                              )
    # contentが取得できていればupdateするため、bodyの内容とdatetime=現在時刻をセット
    else:
        content.body = request.form["body"]
        content.date = datetime.now()

    # contentの内容をaddしてcommit
    db_session.add(content)
    db_session.commit()
    return content.body

if __name__ == "__main__":
    # サーバーの起動
    app.run()
