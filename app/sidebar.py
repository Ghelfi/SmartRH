import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate


def build_sidebar(app: dash.Dash, conf: dict = {}) -> list:

    sidebar = html.Div(
    [
        html.Img(id='toggle_image', src=app.get_asset_url('double_right_arrow_white.png'), className='toggle_image', n_clicks_timestamp=0)
        # dbc.Nav(
        #     [
        #         dbc.NavLink("Home", href="/", active="exact"),
        #         dbc.NavLink("Page 1", href="/page-1", active="exact"),
        #         dbc.NavLink("Page 2", href="/page-2", active="exact"),
        #     ],
        #     vertical=True,
        #     pills=True,
        # ),
    ],
    className="sidebar_div sidebar_div_collapse",
    id='sidebar_div'
)

    return sidebar

def build_sidebar_callbacks(app):
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

    # Change div wisth on click
    @app.callback(
        Output('sidebar_div', 'className'), 
        [Input('toggle_image', 'src')]
        )
    def update_style(src):
        if src == app.get_asset_url('double_right_arrow_white.png'):
            return "sidebar_div sidebar_div_collapse"
        else:
            return "sidebar_div sidebar_div_extended"

