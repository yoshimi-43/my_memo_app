import sys
sys.path.append("/opt/miniconda3/envs/flask_env/lib/python3.13/site-packages")
from flask import Flask
from flask_migrate import Migrate
from models import db, User
from flask_login import LoginManager

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
# loginManagerインスタンス
login_manager = LoginManager()
# LoginManagerとFlaskの紐付け
login_manager.init_app(app)
# 未認証のユーザーがアクセスしようとした際にリダイレクトされる関数名を設定する
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

# viewsのインポート
from views import *

# =====
# 実行
# =====
if __name__ == "__main__":
  app.run()