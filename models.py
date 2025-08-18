from flask_sqlalchemy import SQLAlchemy

# Flask-SQLAlchemyの生成
db = SQLAlchemy()

# =====
# モデル
# =====
# メモ
class Memo(db.Model):
  # テーブル名
  __tablename__ = 'memos'
  # ID(PK)
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  # タイトル(NULL許可しない)
  title = db.Column(db.String(50), nullable=False)
  # 内容
  content = db.Column(db.Text)