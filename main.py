import dash
from dash import html
from app import build_sidebar, build_sidebar_callbacks
from app import menu_layout_mapping_dictionnary, UnderConstructionLayout
from app import my_app
from db import tables

def get_app(config: dict = {}) -> dash.Dash:

    my_app.db.create_all()

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


    build_sidebar_callbacks(my_app(), config=config, display_div_id='display_div')

    return my_app()

if __name__ == '__main__':

    conf = {
        'menu_items': [
            {
                'image': 'search.svg',
                'text': 'Recherche',
            },
            {
                'image': 'window.svg',
                'text': 'Discussion',
            },
            {
                'image': 'transfer.svg',
                'text': 'Transfert',
            },
            {
                'image': 'settings.svg',
                'text': 'Réglages',
            },
            {
                'image': 'settings.svg',
                'text': 'Test',
            },
        ]
    }

    app = get_app(config=conf)
    app.run_server(debug=True)
