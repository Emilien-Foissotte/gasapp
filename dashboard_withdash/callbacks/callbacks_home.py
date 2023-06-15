from app import application

from dash.dependencies import Input, Output, State

@application.callback(
    Output("welcomeuser", "children"),
    Input("userlogged", "data"),
    Input("url_id", "pathname")
)
def welcome_user(data, url):
    if data is None:
        return "### Bienvenue"
    else:
        return f"### Bienvenue {data['username']}"
