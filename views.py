from flask import render_template, request, redirect, url_for
from app import app
from models import db, Memo

# =====
# ルーティング
# =====
# 一覧
@app.route("/memo/")
def index():
  # メモ全件取得
  memos = Memo.query.all()
  # 画面遷移
  return render_template("index.html", memos=memos)

# 登録
@app.route("/memo/create", methods=["GET", "POST"])
def create():
  # POST時
  if request.method == "POST":
    # データ入力取得
    title = request.form["title"]
    content = request.form["content"]
    # 登録処理
    memo = Memo(title=title, content=content)
    db.session.add(memo)
    db.session.commit()
    # 画面遷移
    return redirect(url_for("index"))
  # GET時
  # 画面遷移
  return render_template("create.html")

# 更新
@app.route("/memo/update/<int:memo_id>", methods=["GET", "POST"])
def update(memo_id):
  # データベースからmemo＿idに一致するメモを取得し、
  # 見つからない場合は404エラーを表示
  memo = Memo.query.get_or_404(memo_id)
  # POST時
  if request.method == "POST":
    # 変更処理
    memo.title = request.form["title"]
    memo.content = request.form["content"]
    db.session.commit()
    # 画面遷移
    return redirect(url_for("index"))
  # GET時
  # 画面遷移
  return render_template("update.html", memo=memo)

# 削除
@app.route("/memo/delete/<int:memo_id>")
def delete(memo_id):
  # データベースからmemo＿idに一致するメモを取得し、
  # 見つからない場合は404エラーを表示
  memo = Memo.query.get_or_404(memo_id)
  # 削除処理
  db.session.delete(memo)
  db.session.commit()
  # 画面遷移
  return redirect(url_for("index"))

# モジュールのインポート
from werkzeug.exceptions import NotFound

# エラーハンドリング
@app.errorhandler(NotFound)
def show_404_page(error):
  msg = error.description
  print('エラー内容:',msg)
  return render_template('errors/404.html', msg=msg), 404
