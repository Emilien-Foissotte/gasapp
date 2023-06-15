import app

import core.tasks as core

# core.refresh_database(
# )

ix = core.SpatialIndex()

geoloc = (-0.6789, 47.9217)
list_stations = ix.k_stations(geoloc=geoloc,k=5)

for station in list_stations:
    print(station.to_dict()['ville'])
