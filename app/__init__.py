from flask import Flask
from flask_migrate import Migrate

from app.models.domains import db
from app.Controllers.routes import register_routes


def create_app():
	app = Flask(__name__)
	app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
	app.json.sort_keys = False

	db.init_app(app)
	Migrate(app, db)
	register_routes(app)
	return app


app = create_app()
