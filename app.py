from flask import Flask

from database import db
from routers.usuario_router import usuario_bp
from routers.chamado_router import chamado_bp

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///helpdesk.db"
app.config["SECRET_KEY"] = "troque-esta-chave-em-producao"

db.init_app(app)

app.register_blueprint(usuario_bp)
app.register_blueprint(chamado_bp)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
