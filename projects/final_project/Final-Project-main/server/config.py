import pathlib

import dotenv
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()

mm = Marshmallow()


def create_app():
    this_app = Flask(__name__)
    this_dir = pathlib.Path(__file__)
    dotenv.load_dotenv(this_dir / pathlib.Path(".flaskenv"))
    
    this_app.config.from_prefixed_env()
    db_file = this_dir.parent / pathlib.Path(
        f"{this_app.config['DATABASE_FILE']}.sqlite3"
    )
    this_app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:////{db_file}"
    db.init_app(this_app)
    if not pathlib.Path(this_app.config["SQLALCHEMY_DATABASE_URI"]).exists():
        with this_app.app_context():
            db.create_all()
    with this_app.app_context():
        mm.init_app(this_app)
    return this_app