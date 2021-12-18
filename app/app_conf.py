import dash
import os
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass

@dataclass
class App:
    app: dash.Dash
    db: SQLAlchemy

    def __call__(self) -> dash.Dash:
        return self.app


current_filename = __file__
root_dir = Path(current_filename).parent.parent
assets_dir = os.path.join(root_dir, 'assets')
if not os.path.isdir(assets_dir):
    raise ValueError(f'{assets_dir} does not exists')
else:
    print(f"assets_folders set as {assets_dir}")
dash_app = dash.Dash(__name__, assets_folder=assets_dir)
db = SQLAlchemy(dash_app.server)

dash_app.server.config['SQLALCHEMY_DATABASE_URI'] = os.path.join('sqlite:///'+os.getcwd(), 'test.db')
db = SQLAlchemy(dash_app.server)

my_app = App(dash_app, db)