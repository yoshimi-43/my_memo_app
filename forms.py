from flask import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from models import Memo

# =====
# Formクラス
# =====
# メモ用入力クラス
class MemoForm(FlaskForm):
  # タイトル
  title = StringField('タイトル：', validators=[DataRequired('タイトルは必須入力です'),
                                           Length(max=10, message='10文字以下で入力してください')])
  # 内容
  content = TextAreaField('内容：')
  # ボタン
  submit = SubmitField('送信')

  # カスタムバリデータ
  def validate_title(self, title):
    # StringFieldオブジェクトではなく、その中のデータ(文字列)をクエリに渡す必要があるため
    # 以下のようにtitle.dataを使用して、StirngFieldから実際の文字列データを取得する
    memo = Memo.query.filter_by(title=title.data).first()
    if memo:
      raise ValidationError(f"タイトル '{title.data}' は既に存在します。\
                            別のタイトルを入力してください。")