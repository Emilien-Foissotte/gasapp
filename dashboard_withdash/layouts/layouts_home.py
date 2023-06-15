from dash import dcc, html
import dash_bootstrap_components as dbc
from app import application

navbar = html.Div(
    children=[
        dbc.Nav(
            [
                dbc.NavItem(
                    dbc.NavLink(
                        "Connexion",
                        href="/login",
                        active="exact")
                        ),
                dbc.NavItem(
                    dbc.NavLink(
                        "Mes Stations",
                        href="/stations",
                        active="exact")
                        ),
                dbc.NavItem(
                    dbc.NavLink(
                        "Modifier mes Favoris",
                        href=f"/admin",
                        active="exact"
                        )
                        )
            ],
            className="navbar",
            pills=True,
            justified=True,
            fill=True
        ),
        dcc.Markdown(
            id="welcomeuser",
            style={'color': '#05FA7A'}
            ),
        html.Hr(style={'color': 'white'})
    ]
)

header = html.Div(
    [
        dcc.Markdown(
            "# **CarbuRoam**",
            className="maintitle"
        )
    ]
    )
layout_homepage = html.Div(
    [
        header,
        navbar
    ]
    )
