from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc

from layouts.layouts_home import header, navbar

PAGE_SIZE = 15

layout_price = html.Div(
    [
        header,
        navbar,
        html.Div(
            children=[
                dcc.Interval(
                    id="interval_updateprices",
                    interval=2000
                ),
                dcc.Markdown("## Liste des Prix"),
                dash_table.DataTable(
                    id="price_datatable",
                    style_table={'height': '500px',
                                         'overflowY': 'auto'},
                    style_cell={'background-color': '#ffffff'},
                    cell_selectable=False,
                    page_current=0,
                    page_size=PAGE_SIZE,
                    page_action='custom',

                    filter_action='custom',
                    filter_query='',

                    sort_action='custom',
                    sort_mode='multi',
                    sort_by=[]
                    )
                ],
        style={
            "marginBottom": "4%",
            "marginLeft": "1%",
            "marginRight": "1%"
        }
        ),
        html.Br(),
        html.Div(
        [
            dbc.Collapse(
                id="collapse_message_update",
                is_open=False,
                className="d-grid gap-2 col-2 mx-auto text-center",
                style={"color": "#FF0000"}
                ),
            dbc.Button(
                    "Mettre à jour",
                    id='submit-useradd',
                    n_clicks=0,
                    color="primary",
                    outline=True,
                    size="lg",
                    className="d-grid gap-2 col-2 mx-auto"
                )
        ])
    ])
