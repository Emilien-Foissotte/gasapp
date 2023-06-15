from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import dash_leaflet as dl

from layouts.layouts_home import header, navbar

layout_admin = html.Div(
    [
        header,
        navbar,
        dcc.Markdown("## Mes Options"),
        html.Div(
            children=[
                html.Div(
                [
                    dbc.Collapse(
                        id="collapse_message_delete",
                        is_open=False,
                        className="d-grid gap-2 col-2 mx-auto text-center",
                        style={"color": "#FF0000"}
                        ),
                    dbc.Button(
                            "Supprimer le compte",
                            id='submit-userdel',
                            n_clicks=0,
                            color="danger",
                            outline=True,
                            size="lg",
                            className="d-grid gap-2 col-2 mx-auto"
                        )
                    ]
                )
            ]
        ),
        html.Div(
            children=[
                html.Div(
                    children = [
                        dl.Map(
                            [
                                dl.TileLayer(),
                                dl.LayerGroup(
                                    id="layer_stations",
                                    children = [
                                        dl.GeoJSON(
                                            data=None, id="stations"
                                            )
                                    ]),
                                dl.LocateControl(
                                    options={
                                        'locateOptions': {
                                            'enableHighAccuracy': True
                                            }
                                    }
                                )
                            ],
                            zoom=7,
                            center=(47.82, -2.43),
                            id="map",
                            style={
                                'width': '100%',
                                'height': '90vh',
                                'margin': "auto",
                                "display": "block"}
                            ),
                        html.Div(id="selected_station")
                        ],
                    style={
                        "marginLeft": "1%",
                        "marginRight": "1%"
                        }
                ),
            ]
        )
    ]
)
