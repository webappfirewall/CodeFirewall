#!/usr/bin/env python
# -*- coding: utf-8 -*-
#By: José María HernAndez Estrada & Jason Adair Rossello Romero

import conf_ini
import datetime
from pymongo import MongoClient

#variables globales
client = MongoClient('127.0.0.1', 27017)

def desbloquear():
	db = client['waf']
	collection = db['blacklist']
	collection_log = db['log']

	while True:
		ip = input("\tIntroduce la Ip que deseas desbloquear.\t\t\t\t\tVAWAF:>> ")

		if conf_ini.es_IP_valida(ip):
			break
		else:
			print("\t\tLa Ip no tiene un formato válido.")

	if (collection.find_one_and_delete({"ip" : str(ip)}) == None):
		print("\t\tLa Ip no existe en la BlackList.")
	else:
		descripcion = input("\tIntroduce una descripcion de por que desbloqueas esta Ip.\t\tVAWAF:>> ")
		print("\t\tLa Ip se desbloqueo correctamente.")
		ahora = datetime.datetime.now()
		collection_log.insert_one({"ip":ip,"descripcion":descripcion,"date_at":ahora})

#desbloquear()