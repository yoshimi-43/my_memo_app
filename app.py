from flask import Flask
from flask_migrate import Migrate
from models import db

# =====
# Flask
# =====
app = Flask(__name__)
# 設定ファイル読み込み
app.config.from_object("config.Config")
# dbとFlaskの紐付け
db.init_app(app)
# マイグレーションとの紐付け(Flaskとdb)
migrate = Migrate(app, db)
# viewsのインポート
from views import *

# =====
# 実行
# =====
if __name__ == "__main__":
  app.run()