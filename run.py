from app import FlaskApp, db  # 🔥 Importamos db desde flask_app.py
from app.auth.models import User

# Crear la aplicación usando la clase FlaskApp
app_instance = FlaskApp("dev")
flask_scrapy_app = app_instance.get_app()  # Obtener la instancia de Flask

# Crear las tablas dentro del contexto de la aplicación
with flask_scrapy_app.app_context():
    db.create_all()
    if not User.query.filter_by(user_name="test").first():
        User.create_user(
            user="test",
            email="test-testing@test.com",
            password="andrea1990"
        )

if __name__ == "__main__":
    flask_scrapy_app.run()



# from app import create_app, db
# from app.auth.models import User

# flask_scrapy_app = create_app("prod")
# with flask_scrapy_app.app_context():
#     db.create_all()
    # if not User.query.filter_by(user_name="test").first():