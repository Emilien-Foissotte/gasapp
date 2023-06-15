from flask import Flask, render_template, request, Blueprint, current_app
import requests
import json
import zipfile
from requests.exceptions import HTTPError
import xml.etree.ElementTree as ET
import os
import threading, time, signal
import datetime

APP_BLUEPRINT = Blueprint('app', __name__)

@APP_BLUEPRINT.route("/",  methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        jsondata = main()
        return render_template('gas.html', jsondata = jsondata)
    else:
        try:
            with open('gas.json', 'r') as json_file:
                gasdata = json.load(json_file)
                current_app.logger.info(gasdata)
                return render_template('gas.html', jsondata=gasdata)
        except FileNotFoundError as err:
            return render_template('gas.html', jsondata={})

def loadXML():
    url = "http://donnees.roulez-eco.fr/opendata/instantane"
    try:
        response = requests.get(url, verify=False)
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        print('Success!')

    with open("ZIP.zip", "wb") as ziped:
        ziped.write(response.content)

    with zipfile.ZipFile("ZIP.zip", 'r') as zip_ref:
        zip_ref.extractall("./")

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
        if adresse in add:
            if adresse == add[0]:
                nom = "Total Périph Nantes"
            if adresse == add[1]:
                nom = "Station La Chevrolière"
            if adresse == add[2]:
                nom = "Super U Pt St Martin"
            if adresse == add[3]:
                nom = "Leclerc Chiot"
            if adresse == add[4]:
                nom = "Voisins le Btx"
            if adresse == add[5]:
                nom = "Magny les Hameaux"
            if adresse == add[6]:
                nom = "Total Gif/Yvette"
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

def main():
    loadXML()
    return parseXML('PrixCarburants_instantane.xml')
