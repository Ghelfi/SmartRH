import dash
from dash import html
from app import build_sidebar, build_sidebar_callbacks
from app import menu_layout_mapping_dictionnary, UnderConstructionLayout
from app import my_app
from db import tables, initialize_tables, fill_tables_with_dummy_examples
from extraction import load_extractor
import extraction
from utils import configure_logging
import json
import argparse
import os

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Launch the SmartRH application.')

    root_dir = os.getcwd()

    parser.add_argument('--init_conf_file', type=str, default=os.path.join(root_dir, 'configurations', 'init_conf.json'))
    parser.add_argument('--log_conf_file', type=str, default=os.path.join(root_dir, 'configurations', 'log_conf.json'))
    parser.add_argument('--app_conf_file', type=str, default=os.path.join(root_dir, 'configurations', 'app_conf.json'))

    return parser.parse_args()

def parse_conf_file(args: argparse.Namespace) -> dict:
    
    res_dict = {}
    with open(args.init_conf_file) as fr:
        conf = json.load(fr)
        res_dict = res_dict | conf
    with open(args.log_conf_file) as fr:
        conf = json.load(fr)
        res_dict = res_dict | conf
    with open(args.app_conf_file) as fr:
        conf = json.load(fr)
        res_dict = res_dict | conf

    return res_dict

def get_app(config: dict = {}) -> dash.Dash:
    my_app.db.create_all()
    initialize_tables(my_app, conf["table_initialization"])
    fill_tables_with_dummy_examples(my_app)

    extractor = load_extractor(**conf["ExtractionAlgorithm"])
    my_app.extractor = extractor

    base_layout = html.Div(
        id='root_div',
        className= 'root_div',
        children=[
            build_sidebar(app=my_app(), config=config),
            html.Div(
                id='display_div',
                children=[],
                className='display_div'
            )
        ]
    )
    my_app().layout = base_layout

    for ind, elem in enumerate(config['menu_items']):
        if elem['text'] in menu_layout_mapping_dictionnary:
            config['menu_items'][ind]['children'] = menu_layout_mapping_dictionnary[elem['text']].get_layout()
            menu_layout_mapping_dictionnary[elem['text']].generate_callbacks()
        else :
            config['menu_items'][ind]['children'] = UnderConstructionLayout().get_layout()


    build_sidebar_callbacks(my_app, config=config, display_div_id='display_div')

    return my_app()

if __name__ == '__main__':

    args = parse_args()
    conf = parse_conf_file(args)
    configure_logging(**conf)

    
    
    app = get_app(config=conf)
    app.run_server(debug=True)
