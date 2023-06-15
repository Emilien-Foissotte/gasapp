from typing import List, Optional

from sqlalchemy import (
    create_engine,
    ForeignKey,
    String
    )
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship
    )
engine = create_engine("sqlite:///stations.db")

db = SQLAlchemy(engine)


# transform from Flask-SQLAlchemy to pure SQLAlchemy
class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"

    id = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30)) 

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r})"
    def to_dict():
        return(
        {
            "id": self.id,
            "name": self.name
        }
    

class Carburant(Base):
    __tablename__ = "carburant"

    id = mapped_column(primary_key)
    name: Mapped[str] = mapped_column(String(30))
    xml_id: Mapped[int]

    def __repr__(self) -> str:
        return f"Carburant(id={self.id!r}, name={self.name!r}, xml_id={self.xml_id!r})"
    def to_dict():
        return(
        {
            "id": self.id,
            "name": self.name,
            "xml_id": self.xml_id
        }

class Price(Base):
    __tablename__ = "price"

    id = mapped_column(primary_key)
    date = Mapped[datetime]
    carburant_id: Mapped[int] = mapped_column(ForeignKey("carburant.id"))
    carburant: Mapped["Carburant"] = relationship(back_populates="price")

class Station(Base):
    __tablename__ = "station"

    id = mapped_column(primary_key)
    name: Mapped[Optionale[str]]
    address = Mapped[str]
    ville = Mapped[str]
    zipcode = Mapped[int]
    latitude = Mapped[float]
    longitude = Mapped[float] 

class Station(db.Model):
    """
    A model for the movements table in database.
    """
    id = db.Column(db.Text, primary_key=True)
    address = db.Column(db.Text)
    ville = db.Column(db.Text)
    zipcode = db.Column(db.Integer)

    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)

    SP95 = db.Column(db.Float)
    updateSP95 = db.Column(db.DateTime)
    SP98 = db.Column(db.Float)
    updateSP98 = db.Column(db.DateTime)
    GAZOLE = db.Column(db.Float)
    updateGAZOLE = db.Column(db.DateTime)
    E10 = db.Column(db.Float)
    updateE10 = db.Column(db.DateTime)
    GPLC = db.Column(db.Float)
    updateGPLC = db.Column(db.DateTime)
    E10 = db.Column(db.Float)
    updateE10 = db.Column(db.DateTime)
    E85 = db.Column(db.Float)
    updateE85 = db.Column(db.DateTime)


    def to_geodict(self):
        ret_dict = {
            "lat": self.latitude/100000,
            "lon": self.longitude/100000,
            "name": f"{self.address} - {self.zipcode} - {self.ville}",
            "id": self.id
        }
        return ret_dict

    def to_dict(self):
        ret_dict = {
            "id": self.id,
            "address": self.address,
            "ville": self.ville,
            "zipcode": self.zipcode,
            "SP95": self.SP95,
            "updateSP95": self.updateSP95,
            "SP98": self.SP98,
            "updateSP98": self.updateSP98,
            "GAZOLE": self.GAZOLE,
            "updateGAZOLE": self.updateGAZOLE,
            "E10": self.E10,
            "updateE10": self.updateE10,
            "GPLC": self.GPLC,
            "updateGPLC": self.updateGPLC,
            "latitude": self.latitude,
            "longitude": self.longitude
        }
        return ret_dict

class TrackStation(db.Model):
    user_id = db.Column(db.Text, db.ForeignKey(User.id), primary_key=True)
    station_id = db.Column(db.Text, db.ForeignKey(Station.id), primary_key=True)

conf_essence = {
    'GAZOLE': 1,
    'SP95': 2,
    'E85': 3,
    'E10': 5,
    'SP98': 6,
    'GPLC': 4
    }


class SpatialIndex:
    def __init__(self):
        self.stations = {} # indexed by stations id
        self.stations_spatial_index = index.Index(
            properties=index.Property(
                dimension=2
            )
        )

        self._index_stations()

    def _index_stations(self):
        tot_lon = 0
        # iterate through all nodes
        for station in Station.query.all():
            self.stations[int(station.id)] = station
            tot_lon += station.longitude

            self.stations_spatial_index.insert(
                int(station.id), (station.longitude, station.latitude)
                )
        n_items = len(self.stations.items())

    def k_stations(self, geoloc, k):
        stations_candidates = []
        search_dist, increment = (10000, 10000)
        while len(stations_candidates) < k:
            stations_candidates = self.candidate_stations(
                geoloc=geoloc,
                max_dist=search_dist
                )
            search_dist += increment
        return stations_candidates


    def candidate_stations(self, geoloc, max_dist):  # was (lat,lon) in place of geoloc
            (lon, lat) = geoloc

            easting_utm, northing_utm, zone_number, zone_letter = utm.from_latlon(
                lat,
                lon
                )
            lat_max, lon_max = utm.to_latlon(
                easting_utm + max_dist,
                northing_utm + max_dist,
                zone_number,
                zone_letter
                )

            lat_min, lon_min = utm.to_latlon(
                easting_utm - max_dist,
                northing_utm - max_dist,
                zone_number,
                zone_letter
                )
            lat_min = lat_min * 100000
            lon_min = lon_min * 100000
            lat_max = lat_max * 100000
            lon_max = lon_max * 100000


            nearby_states = self.stations_spatial_index.intersection((lat_min,
                                                                   lon_min,
                                                                   lat_max,
                                                                   lon_max))

            stations_candidates_list = [self.stations[id] for id in nearby_states]
            return stations_candidates_list

ix = SpatialIndex()