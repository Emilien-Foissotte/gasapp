import re
import sys
import uuid
import urllib
from app import application, db, User, ix, TrackStation
import sys

from dash import ctx
from dash.dependencies import Input, Output, State
import dash_leaflet as dl
import dash_leaflet.express as dlx


@application.callback(
    Output("collapse_message_delete", "chilren"),
    State("userlogged", "data"),
    Input("submit-userdel", "n_clicks"),
    )
def delete_user(data, submit):
    userlogged = data["username"]
    if submit:
        deleteuser = User.query.filter_by(name=username).first()
        db.session.delete(deleteuser)
        db.session.commit()
    return ""


@application.callback(
    [Output("stations", "data"),
     Output("stations", "zoomToBounds")],
    [State("userlogged", "data"),
     Input("stations", "click_feature"),
     Input("map", "click_lat_lng")
     ])
def map_station_click(data, stationcliked, click_lat_lng):
    username = data["username"]
    if ctx.triggered_id == "stations" and not stationcliked is None:
        addstation_user = User.query.filter_by(name=username).first()

        track = TrackStation.query.filter(
            TrackStation.user_id == addstation_user.id,
            TrackStation.station_id == stationcliked['properties']['id']
        ).first()
        if track is None:
            requested_track = TrackStation(
                user_id=addstation_user.id,
                station_id=stationcliked['properties']['id']
            )
            action = "added"
            db.session.add(requested_track)
            db.session.commit()
        else:
            action = "deleted"
            db.session.delete(track)
            db.session.commit()

        zoom = False
        lon ,lat = stationcliked['geometry']['coordinates'][0], stationcliked['geometry']['coordinates'][1]

    else:
        lat, lon = click_lat_lng
        zoom = True

    geoloc = (lat, lon)

    list_stations = ix.k_stations(geoloc=geoloc,k=10)

    stations = [station.to_geodict() for station in list_stations]
    followed_stations = []
    followuser = User.query.filter_by(name=username).first()
    for station in stations:
        track = TrackStation.query.filter(
            TrackStation.user_id == followuser.id,
            TrackStation.station_id == station['id']
        ).first()
        if track is None:

            station['name'] = station['name'] + "\n [FOLLOW]"
        else:
            station['name'] = station['name'] + "\n [UNFOLLOW]"
        followed_stations.append(station)

    geojson = dlx.dicts_to_geojson([{**c, **dict(tooltip=c['name'])} for c in followed_stations])

    return geojson, zoom




def encode_targeturl(path_number, **kwargs):
    query = "fueltraj?%s" % urllib.parse.urlencode({
        "id": kwargs['id'],
        "path_number": path_number
        })
    ret_str = f'<a href="{kwargs["urlprefix"] + query}" target="_blank"><center><img align="center" height="22" src="{img_icon_goto}"></center></a>'
    return ret_str
