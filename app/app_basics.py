import dash
from .sidebar import build_sidebar, build_sidebar_callbacks
import os
from pathlib import Path

def get_app(config: dict = {}) -> dash.Dash:
    current_filename = __file__
    root_dir = Path(current_filename).parent.parent
    assets_dir = os.path.join(root_dir, 'assets')
    if not os.path.isdir(assets_dir):
        raise ValueError(f'{assets_dir} does not exists')
    else:
        print(f"assets_folders set as {assets_dir}")
    app = dash.Dash(__name__, assets_folder=assets_dir)

    app.layout = build_sidebar(app=app)
    build_sidebar_callbacks(app)

    return app