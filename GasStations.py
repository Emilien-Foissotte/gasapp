# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 13:49:08 2020

@author: S609333
"""



import requests
import json
import zipfile
from requests.exceptions import HTTPError
import xml.etree.ElementTree as ET 
import os
import threading, time, signal
from datetime import timedelta


# Interval du temps pour chaque execution (en seconde)
WAIT_TIME_SECONDS = int(2*10800)    # 6 heures

def loadXML():
    urls = ["https://donnees.roulez-eco.fr/opendata/instantane"]
    for url in urls:
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
                    mydict = {
                        "nom": nom,
                        "essence": essence,
                        "prix": valeur
                        }
                    #print(nom, prix.get('nom'), float(prix.get('valeur')))
                    reslst.append(mydict)
    res.update({"stations": reslst})
    with open('/var/www/html/gas.json', 'w') as json_file:
        print(res)
        json.dump(res, json_file)

def main():
    loadXML()        
    parseXML('PrixCarburants_instantane.xml')


class ProgramKilled(Exception):
    pass

def signal_handler(signum, ffoorame):
    raise ProgramKilled          

class Job(threading.Thread):
    def __init__(self, interval, execute, *args, **kwargs):
        threading.Thread.__init__(self)
        self.daemon = False
        self.stopped = threading.Event()
        self.interval = interval
        self.execute = execute
        self.args = args 
        self.kwargs = kwargs
        
    def stop(self):
                self.stopped.set()
                self.join()
    def run(self):
        while not self.stopped.wait(self.interval.total_seconds()):
            self.execute(*self.args, **self.kwargs)
            
if __name__ == "__main__":
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    job = Job(interval=timedelta(seconds=WAIT_TIME_SECONDS), execute=main)
    job.start()

    while True:
        try:
            time.sleep(1)
        except ProgramKilled:
            print("Program killed: running cleanup code")
            job.stop()
            break




        
loadXML()        
parseXML('PrixCarburants_instantane.xml')
    
    
    
    
    
    # with open("PrixCarburants_instantane.xml") as xml_file: 
    #     data_dict = xmltodict.parse(xml_file.read()) 
    #     xml_file.close() 
    #os.remove("./PrixCarburants_instantane.xml")
    # generate the object using json.dumps()  
    # corresponding to json data 
      
    # json_data = json.dumps(data_dict) 
      
    ## Write the json data to output  
    ## json file 
    # with open("data.json", "w") as json_file: 
    #     json_file.write(json_data) 
    #     json_file.close()

# with open('data.json', 'r') as f:
#   dict_data = json.load(f)

# for key, val in dict_data.items():
#     print(key, "=>", val)
    