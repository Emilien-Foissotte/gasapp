from dash import dcc, html
import dash_bootstrap_components as dbc

from layouts.layouts_home import header, navbar


layout_login = html.Div(
    [
        header,
        navbar,
        dcc.Markdown("## Connexion"),
        html.Div(
            children=[
                dcc.Markdown("#### Se connecter :"),
                dcc.Interval(
                    id="interval_updateusers",
                    interval=2000
                ),
                dcc.Dropdown(
                    id="selected_user",
                    value=None,
                    multi=False,
                    clearable=False,
                    persistence=True
                    ),
                ],
                style={
                    "width": "20%",
                    "marginLeft": "1%",
                    "marginRight": "1%"
                    }
            ),
        html.Hr(style={'color': 'white'}),
        html.Div(
            children=[
                dcc.Markdown("#### Ajouter un utilisateur :"),
                dcc.Input(
                    id="useradd_input",
                    type="text",
                    value="",
                    placeholder="Entrez un nom",
                )],
                style={
                    "width": "20%",
                    "marginLeft": "1%",
                    "marginRight": "1%"
                    }
                ),
        html.Div(
        [
            dbc.Collapse(
                id="collapse_message_useradd",
                is_open=False,
                className="d-grid gap-2 col-2 mx-auto text-center",
                style={"color": "#FF0000"}
                ),
            dbc.Button(
                    "Ajouter",
                    id='submit-useradd',
                    n_clicks=0,
                    color="primary",
                    outline=True,
                    size="lg",
                    className="d-grid gap-2 col-2 mx-auto"
                )
            ]
        )
    ]
)
