from datetime import timedelta
import json
import os
import xml.etree.ElementTree as ET
import zipfile

import requests
from requests.exceptions import HTTPError
import streamlit as st

from spatial_tools import Station

def loadXML():
    urls = ["https://donnees.roulez-eco.fr/opendata/instantane"]
    for url in urls:
        try:
            response = requests.get(url, verify=False)
            # If the response was successful, no Exception will be raised
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            print('Success!')
    ziped = open("ZIP.zip", "wb")
    ziped.write(response.content)
    ziped.close()
    with zipfile.ZipFile("ZIP.zip", 'r') as zip_ref:
        zip_ref.extractall("./")
        zip_ref.close()
    os.remove("ZIP.zip")

def parseXML(xmlfile):
    # create element tree object
    tree = ET.parse(xmlfile)

    # get root element
    root = tree.getroot()

     # create empty list for pdv
    trackids = []
    add = ['226 BLD DE LA LOIRE', '78 Grand\'Rue', 'Rue des Vignes', 'AVENUE GEORGES POMPIDOU','RUE AUX FLEURS', 'PLACE DE BEAUPLAN', '155 AVENUE DU GENERAL LECLERC']
    res = dict()
    reslst = []
    station=0
    for pdv in root.findall('pdv'):
        ident = int(pdv.get('id'))
        adresse = pdv.find('adresse').text
        latitude = float(pdv.get('latitude'))
        longitude = float(pdv.get('longitude'))
            for prix in pdv.findall('prix'):
                if prix.get('id') == "2" or prix.get('id') == "5":
                    station+=1
                    essence = prix.get('nom')
                    valeur = float(prix.get('valeur'))
                    valmaj = prix.get('maj')
                    time = datetime.datetime.strptime(valmaj,"%Y-%m-%d %H:%M:%S")
                    maj = time.strftime("%d/%m")
                    mydict = {
                        "nom": nom,
                        "essence": essence,
                        "prix": str(valeur)+" €",
                        "maj": maj
                        }
                    #print(nom, prix.get('nom'), float(prix.get('valeur')))
                    reslst.append(mydict)
    res.update({"stations": reslst})
    with open('gas.json', 'w') as json_file:
        print(res)
        json.dump(res, json_file, indent=4)
    return res

def refresh_database(
    id_list=[]
    ):
    filter = len(id_list) > 0
    # loadXML()
    xmlfile = 'PrixCarburants_instantane.xml'
    # create element tree object
    tree = ET.parse(xmlfile)

    # get root element
    root = tree.getroot()

    # parse stations from configuration
    with open('conf_stations.json', 'r') as confile:
        conf_stations = json.load(confile)
    # select only ids specified under configuraton
    idents = [station["ident"] for station in conf_stations["stations"]]
    # loop over each point de vente
    for pdv in tqdm(root.findall('pdv')):
        if filter and pdv.get('id') in id_list or not filter:
            # query station to see if it's in the database
            station = Station.query.filter_by(
                id=int(pdv.get('id'))
                ).first()
            # if not, create it
            if station is None:
                station = Station()
            # apply some transformations
            for elem in pdv:
                if elem.tag == 'adresse':
                    station.address = elem.text.upper()
                elif elem.tag == 'ville':
                    station.ville = elem.text.upper()
            # update other relevant fields
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
    # load file from instant data feed
    #loadXML()
