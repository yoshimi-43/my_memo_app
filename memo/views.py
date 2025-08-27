from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Memo
from forms import MemoForm
from flask_login import login_required

# memoのBlueprint
memo_bp = Blueprint('memo', __name__, url_prefix='/memo')

# =====
# ルーティング
# =====
# 一覧
@memo_bp.route("/")
@login_required
def index():
  # メモ全件取得
  memos = Memo.query.all()
  # 画面遷移
  return render_template("memo/index.html", memos=memos)

# 登録(Form使用)
@memo_bp.route("/create", methods=["GET", "POST"])
@login_required
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
    return redirect(url_for("memo.index"))
  # GET時
  # 画面遷移
  return render_template("memo/create_form.html", form=form)

# 更新(Form使用)
@memo_bp.route("/update/<int:memo_id>", methods=["GET", "POST"])
@login_required
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
    return redirect(url_for("memo.index"))
  # GET時
  # 画面遷移
  return render_template("memo/update_form.html", form=form, edit_id = target_data.id)

# 削除
@memo_bp.route("/delete/<int:memo_id>")
@login_required
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
  return redirect(url_for("memo.index"))