import dash
import os
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy, Model
from dataclasses import dataclass
from extraction import GenericExtractor

@dataclass
class App:
    app: dash.Dash
    db: SQLAlchemy
    extractor: GenericExtractor = None

    def __call__(self) -> dash.Dash:
        return self.app

    def add_to_db(self, elem: Model):
        try:
            self.db.session.add(elem)
            self.db.session.commit()
        except:
            self.db.session.rollback()

    def query(self, elem: Model):
        return self.db.session.query(elem)


current_filename = __file__
root_dir = Path(current_filename).parent.parent
assets_dir = os.path.join(root_dir, 'assets')
if not os.path.isdir(assets_dir):
    raise ValueError(f'{assets_dir} does not exists')
dash_app = dash.Dash(__name__, assets_folder=assets_dir)

dash_app.server.config['SQLALCHEMY_DATABASE_URI'] = os.path.join('sqlite:///'+os.getcwd(), 'test.db')
dash_app.server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(dash_app.server)

my_app = App(dash_app, db)