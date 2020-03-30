#!/usr/bin/env python
# -*- coding: utf-8 -*-
#By: José María HernAndez Estrada & Jason Adair Rossello Romero

import urllib.parse
from pymongo import MongoClient
import conexiondb

# Variables globales
client = conexiondb.client

def checar_duplicidad(coleccion, ip):
	db = client['waf']
	collection = db[coleccion]
	if(collection.find_one({"ip" : ip}) == None):
	#el dato es unico
		return True
	else:
	#el dato esta repetido
		return False

def esta_en_bl(ip):
	db = client['waf']
	collection = db['blacklist']
	if(collection.find_one({"ip" : ip}) == None):
	#el dato no esta en la bl
		return True
	else:
	#el dato esta en la bl
		return False

def buscaBorra(ip, coleccion):
	db = client['waf']
	collection = db[coleccion]
	if (collection.find_one_and_delete({"ip": ip}) == None):
		# el dato no esta en la bl
		return True
	else:
		# el dato esta en la bl
		print('\t\t\tIp eliminada de la WhiteList: ' + ip)
		return False

#checar_duplicidad("whitelist", "127.0.0.100")