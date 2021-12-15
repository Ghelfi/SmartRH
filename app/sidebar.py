import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import json
import numpy as np


def build_sidebar(app: dash.Dash, config: dict = {}) -> list:

    menu_items = config['menu_items']

    menu_items_render = [
        html.Div(
            id='menu_item_{}_div'.format(ind),
            className='menu_item_div_base menu_item_div_unselected',
            n_clicks_timestamp=0,
            children=[
                html.Img(id='menu_item_{}_img'.format(ind), src=app.get_asset_url(elem['image']), className='menu_image'),
                html.P(elem['text'], id='menu_item_{}_text'.format(ind), className='menu_text menu_color menu_text_collapse')
            ],
            style={'top': '{}rem'.format(int((ind+1)*3))})
        for ind,elem in enumerate(menu_items)
    ]

    sidebar = html.Div(
    [
        html.Img(id='toggle_image', src=app.get_asset_url('double_right_arrow_white.png'), className='toggle_image', n_clicks_timestamp=0)
    ] + menu_items_render,
    className="sidebar_div sidebar_div_collapse",
    id='sidebar_div'
)

    return sidebar

def build_sidebar_callbacks(app, display_div_id: str, config: dict= {}):

    menu_items = config['menu_items']


    # Change toggle icon on click
    @app.callback(
    Output('toggle_image', 'src'),
    [Input('toggle_image', 'n_clicks_timestamp')],
    [State('toggle_image', 'src')])
    def change_img(click, src):
        if not click: raise PreventUpdate

        if src == app.get_asset_url('double_right_arrow_white.png'):
            return app.get_asset_url('double_left_arrow_white.png')
        
        else:
            return app.get_asset_url('double_right_arrow_white.png')

    # Change div width on click
    @app.callback(
        Output('sidebar_div', 'className'), 
        [Input('toggle_image', 'src')]
        )
    def update_style(src):
        if src == app.get_asset_url('double_right_arrow_white.png'):
            return "sidebar_div sidebar_div_collapse"
        else:
            return "sidebar_div sidebar_div_extended"

    # Change Menu Item text visibility on click
    @app.callback(
    [Output('menu_item_{}_text'.format(ind), 'className') for ind in range(len(menu_items))], 
    [Input('toggle_image', 'src')]
    )
    def update_text_style(src):
        if src == app.get_asset_url('double_right_arrow_white.png'):
            return ["menu_text menu_text_collapse" for e in menu_items]
        else:
            return ["menu_text menu_text_extended" for e in menu_items]

    # Change Menu Item background if selected
    @app.callback(
    [Output('menu_item_{}_div'.format(e), 'className') for e in range(len(menu_items))],
    [Input('menu_item_{}_div'.format(e), 'n_clicks_timestamp') for e in range(len(menu_items))],
    )
    def update_div_style_on_click(*args):
        res = ["menu_item_div_base menu_item_div_unselected"  for e in menu_items]
        ctx = dash.callback_context
        trigerred_id = ctx.triggered[0]['prop_id']
        try:
            trigerred_id = ctx.triggered[0]['prop_id']
            id_ = int(trigerred_id.split('.')[0].split('_')[-2])
        except:
            id_ = 0
        res[id_] = "menu_item_div_base menu_item_div_selected"
        return tuple(res)

    # Change The display div children depending on the pressed button
    @app.callback(
    Output(display_div_id, 'children'),
    [Input('menu_item_{}_div'.format(e), 'n_clicks_timestamp') for e in range(len(menu_items))],
    )
    def update_display_div_children(*args):
        ctx = dash.callback_context
        trigerred_id = ctx.triggered[0]['prop_id']
        try:
            trigerred_id = ctx.triggered[0]['prop_id']
            id_ = int(trigerred_id.split('.')[0].split('_')[-2])
        except:
            id_ = 0
        return menu_items[id_]['children']
