from flask import render_template, request, redirect, url_for, flash
from app import app
from models import db, Memo
from forms import MemoForm

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

# 登録(Form使用)
@app.route("/memo/create", methods=["GET", "POST"])
def create():
  # Formインスタンス生成
  form = MemoForm()
  if form.validate_on_submit():
    # データ入力取得
    title = form.title.data
    content = form.content.data
    # 登録処理
    memo = Memo(title=title, content=content)
    db.session.add(memo)
    db.session.commit()
    # フラッシュメッセージ
    flash("登録しました")
    # 画面遷移
    return redirect(url_for("index"))
  # GET時
  # 画面遷移
  return render_template("create_form.html", form=form)

# 更新(Form使用)
@app.route("/memo/update/<int:memo_id>", methods=["GET", "POST"])
def update(memo_id):
  # データベースからmemo＿idに一致するメモを取得し、
  # 見つからない場合は404エラーを表示
  target_data = Memo.query.get_or_404(memo_id)
  # Formに入れ替え
  form = MemoForm(obj=target_data)

  if request.method == "POST" and form.validate():
    # 変更処理
    target_data.title = form.title.data
    target_data.content = form.content.data
    db.session.commit()
    # フラッシュメッセージ
    flash("変更しました")
    # 画面遷移
    return redirect(url_for("index"))
  # GET時
  # 画面遷移
  return render_template("update_form.html", form=form, edit_id = target_data.id)

# 削除
@app.route("/memo/delete/<int:memo_id>")
def delete(memo_id):
  # データベースからmemo＿idに一致するメモを取得し、
  # 見つからない場合は404エラーを表示
  memo = Memo.query.get_or_404(memo_id)
  # 削除処理
  db.session.delete(memo)
  db.session.commit()
  # フラッシュメッセージ
  flash("削除しました")
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
