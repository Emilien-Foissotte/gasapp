import logging

from app import application, server

from dash import dcc
from dash.dependencies import Input, Output
from dash import html

from callbacks.callbacks_pricelist import *
from callbacks.callbacks_admin import *
from callbacks.callbacks_login import *
from callbacks.callbacks_home import *

from layouts.layouts_home import *
from layouts.layouts_login import *
from layouts.layouts_prices import *
from layouts.layouts_admin import *

logger = logging.getLogger(__name__)


application.layout = html.Div([
    dcc.Store(
        id="userlogged",
        storage_type="local"
        ),
    dcc.Location(
        id="url_id",
        refresh=False
    ),
    html.Div(
        id="page-content"
    )
])

@application.callback(
    Output("page-content", "children"),
    [Input("userlogged", "data"),
     Input("url_id", "pathname")])
def display_page(data, pathname):
    if data is None:
        return layout_login
    elif pathname == "/" or pathname =="/login":
        return layout_login
    elif pathname == "/stations":
        return layout_price
    elif pathname == "/admin":
        return layout_admin

if __name__ == "__main__":
    application.run_server(
        debug=True,
        port="8050",
        host="0.0.0.0"
    )
else:
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        format=(
            "%(asctime)s %(name)-12s %(module)s.%(funcName)s "
            "%(processName)s %(levelname)-8s %(relativeCreated)d %(message)s"),
        level=logging.INFO,
    )
    gunicorn_logger = logging.getLogger('gunicorn.error')
    # create app logger
    server_logger = create_logger(application.server)
    # extend the Flask handlers with those of gunicorn
    application.logger.handlers = logger.handlers
    server_logger.handlers = logger.handlers
    application.logger.setLevel(logger.level)
    application.logger.info(
        "Initializing server..."
    )
    logger.handlers = gunicorn_logger.handlers

    server = application.server
