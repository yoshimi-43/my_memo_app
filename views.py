from flask import render_template, request, redirect, url_for, flash
from app import app
from models import db, Memo, User
from forms import MemoForm, LoginForm, SignUpForm
from flask_login import login_user, logout_user

# =====
# ルーティング
# =====
# ログイン(Form使用)
@app.route("/", methods=["GET", "POST"])
def login():
  # Formインスタンス生成
  form = LoginForm()
  if form.validate_on_submit():
    # データ入力取得
    username = form.username.data
    password = form.password.data
    # 対象User取得
    user = User.query.filter_by(username=username).first()
    # 認証判定
    if user is not None and user.check_password(password):
      # 成功
      # 引数として渡されたuserオブジェクトを使用して、ユーザーをログイン状態にする
      login_user(user)
      # 画面遷移
      return redirect(url_for("index"))
    # 失敗
    flash("認証不備です")
  # GET時
  # 画面遷移
  return render_template("login_form.html", form=form)

# ログアウト
@app.route("/logout")
def logout():
  # 現在ログインしているユーザーをログアウトする
  login_user()
  # フラッシュメッセージ
  flash("ログアウトしました")
  # 画面遷移
  return redirect(url_for("login"))

# サインアップ
@app.route("/register", methods=["GET", "POST"])
def register():
  # Formインスタンス生成
  form = SignUpForm()
  if form.validate_on_submit():
    # データ入力取得
    username = form.username.data
    password = form.password.data
    # モデルを生成
    user = User(username=username)
    # パスワードハッシュ化
    user.set_password(password)
    # 登録処理
    db.session.add(user)
    db.session.commit()
    # フラッシュメッセージ
    flash("ユーザー登録しました")
    # 画面遷移
    return redirect(url_for("login"))
  # GET時
  # 画面遷移
  return render_template("register_form.html", form=form)

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
