#!/usr/bin/env python
# -*- coding: utf-8 -*-
#By: José María HernAndez Estrada & Jason Adair Rossello Romero

import urllib.parse
from pymongo import MongoClient
import conexiondb

# Variables globales
client = conexiondb.client
db = client['waf']

def showcoll(coleccion):
    collection = db[coleccion]

    if collection.find() != None:
        datos = collection.find()
        i = 1
        for dato in datos:
            print("\t" + str(i) + ". Ip:\t" + dato['ip'])
            i += 1
    else:
        print("La base de datos aun no tiene elementos guardados.")

#showcoll('blacklist')