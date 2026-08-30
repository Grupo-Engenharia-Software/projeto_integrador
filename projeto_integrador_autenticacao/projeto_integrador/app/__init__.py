"""
Application factory: função que cria e configura a instância do Flask.

Usar uma factory (em vez de instanciar o Flask direto no módulo) facilita
testes e evita importação circular entre extensões, models e controllers.
"""
from flask import Flask

from app.config import Config
from app.extensions import db, login_manager, csrf, limiter


def create_app(config_class: type = Config) -> Flask:
    app = Flask(__name__, template_folder="views", static_folder="static")
    app.config.from_object(config_class)

    # Inicializa as extensões com a instância da aplicação
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)

    # Registra os Blueprints (grupos de rotas dos Controllers)
    from app.controllers.auth_controller import auth_bp
    from app.controllers.main_controller import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    # Cria as tabelas no banco caso ainda não existam
    with app.app_context():
        db.create_all()

    return app


# Necessário para o Flask-Login saber como carregar um usuário a partir
# do id guardado na sessão (cookie assinado, nunca a senha).
@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))
