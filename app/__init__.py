import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

# 🔥 Definir instancias globales para ser reutilizadas en todos los archivos
db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
bcrypt = Bcrypt()

class FlaskApp:
    def __init__(self, config_type):
        """Inicializa la aplicación Flask con la configuración especificada."""
        self.app = Flask(__name__)
        self.config_type = config_type
        self.configure_app()
        self.register_blueprints()

    def configure_app(self):
        """Carga la configuración y configura las extensiones."""
        configuration = os.path.join(os.getcwd(), "config", self.config_type + ".py")
        self.app.config.from_pyfile(configuration)

        # 🔥 Inicializamos las extensiones con la aplicación Flask
        db.init_app(self.app)
        bootstrap.init_app(self.app)
        login_manager.init_app(self.app)
        bcrypt.init_app(self.app)

        # Configuración adicional de Flask-Login
        login_manager.login_view = "authentication.log_in_user"
        login_manager.session_protection = "strong"

    def register_blueprints(self):
        """Registra los Blueprints en la aplicación."""
        from app.auth import authentication
        self.app.register_blueprint(authentication)

    def get_app(self):
        """Devuelve la instancia de la aplicación Flask."""
        return self.app

# import os 
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_bootstrap import Bootstrap
# from flask_login import LoginManager
# from flask_bcrypt import Bcrypt

# db = SQLAlchemy()
# bootstrap = Bootstrap()
# login_manager = LoginManager()
# bcrypt = Bcrypt()
# login_manager.login_view = "authentication.log_in_user"
# login_manager.session_protection = "strong"

# def create_app(config_type):
#     app = Flask(__name__)
#     configuration = os.path.join(os.getcwd(), "config", config_type + ".py")
#     app.config.from_pyfile(configuration)
#     db.init_app(app)
#     bootstrap.init_app(app)
#     login_manager.init_app(app)
#     bcrypt.init_app(app)
#     from app.auth import authentication
#     app.register_blueprint(authentication)
#     return app
