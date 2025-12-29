from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from logging import Logger, getLogger

from config import Config

# Объект SQLAlchemy для работы с БД
db = SQLAlchemy()
# Объект для работы с миграциями
migrate = Migrate()
# Настройки логгирования
logger: Logger = getLogger(__name__)

# Создание объекта приложения
app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)

# Регистрация ендпоинтов
from app.routes.main import bp as main_bp

app.register_blueprint(main_bp)
