from datetime import datetime
import json
import os
import xml.etree.ElementTree as ET
import zipfile

import requests
from requests.exceptions import HTTPError
from tqdm import tqdm

from app import db, Station, ix

def string_to_date(dbstring):
    if dbstring is None:
        return datetime.strptime(
            "1970-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"
        )
    else:
        return datetime.strptime(
            dbstring, "%Y-%m-%d %H:%M:%S"
        )

def refresh_database(
    id_list=[]
    ):
    filter = len(id_list) > 0
    # # fetch the xml file from the updated flux
    # url = "http://donnees.roulez-eco.fr/opendata/instantane"
    # try:
    #     response = requests.get(url, verify=False)
    #     # If the response was successful, no Exception will be raised
    #     response.raise_for_status()
    # except HTTPError as http_err:
    #     print(f'HTTP error occurred: {http_err}')  # Python 3.6
    # except Exception as err:
    #     print(f'Other error occurred: {err}')  # Python 3.6
    # else:
    #     print('Success!')
    #
    # with open("ZIP.zip", "wb") as ziped:
    #     ziped.write(response.content)
    #
    # with zipfile.ZipFile("ZIP.zip", 'r') as zip_ref:
    #     zip_ref.extractall("./")
    #
    # os.remove("ZIP.zip")
    xmlfile = 'PrixCarburants_instantane.xml'
    # create element tree object
    tree = ET.parse(xmlfile)

    # get root element
    root = tree.getroot()

    # parse all stations
    with open('conf_stations.json', 'r') as confile:
        conf_stations = json.load(confile)
    idents = [station["ident"] for station in conf_stations["stations"]]
    for pdv in tqdm(root.findall('pdv')):
        if filter and pdv.get('id') in id_list or not filter:
            station = Station.query.filter_by(
                id=int(pdv.get('id'))
                ).first()
            if station is None:
                station = Station()
            for elem in pdv:
                if elem.tag == 'adresse':
                    station.address = elem.text.upper()
                elif elem.tag == 'ville':
                    station.ville = elem.text.upper()

            station.id = int(pdv.get('id'))
            station.longitude = float(pdv.get('longitude'))
            station.latitude = float(pdv.get('latitude'))
            station.zipcode = int(pdv.get('cp'))
            for prix in pdv.findall('prix'):
                essence = prix.get('nom')
                if essence == "E10":
                    station.E10 = float(prix.get('valeur'))
                    station.updateE10 = string_to_date(prix.get('maj'))
                elif essence == "E85":
                    station.E85 = float(prix.get('valeur'))
                    station.updateE85 = string_to_date(prix.get('maj'))
                elif essence == "GPLc":
                    station.GPLC = float(prix.get('valeur'))
                    station.updateGPLC = string_to_date(prix.get('maj'))
                elif essence == "SP95":
                    station.SP95 = float(prix.get('valeur'))
                    station.updateSP95 = string_to_date(prix.get('maj'))
                elif essence == "SP98":
                    station.SP98 = float(prix.get('valeur'))
                    station.updateSP98 = string_to_date(prix.get('maj'))
                elif essence == "Gazole":
                    station.GAZOLE = float(prix.get('valeur'))
                    station.updateGAZOLE = string_to_date(prix.get('maj'))
            db.session.add(station)
            db.session.commit()

if __name__ == "__main__":
    refresh_data()
