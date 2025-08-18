# =====
# 設定
# =====
class Config(object):
  # デバッグモード
  DEBUG=True
  # 警告対策
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  # DB設定
  SQLALCHEMY_DATABASE_URI = "sqlite:///memodb.sqlite"