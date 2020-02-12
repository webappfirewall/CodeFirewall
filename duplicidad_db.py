#!/usr/bin/env python
# -*- coding: utf-8 -*-
#By: José María HernAndez Estrada & Jason Adair Rossello Romero

from pymongo import MongoClient

#variables globales
client = MongoClient('127.0.0.1', 27017)

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

#checar_duplicidad("whitelist", "127.0.0.100")