#!/usr/bin/env python
# -*- coding: utf-8 -*-
#By: José María HernAndez Estrada & Jason Adair Rossello Romero

import urllib.parse
import conf_ini
import datetime
import muestraColecciones
from pymongo import MongoClient

#variables globales
username = urllib.parse.quote_plus('@dm1n')
passwor = urllib.parse.quote_plus('Qw3rt&12345')
client = MongoClient('mongodb://%s:%s@10.0.2.4' % (username, passwor))

def desbloquear():
	db = client['waf']
	collection = db['blacklist']
	collection_log = db['log']

	while True:
		ip = input("\tIntroduce la Ip que deseas desbloquear.\t\t\t\t\tVAWAF:>> ")

		#permite regresar con back
		if ip == "back" or ip == "BACK":
			break
		# con el comando show muestra todas las ip contenidas en la base de datos
		elif ip == "show":
			muestraColecciones.showcoll('blacklist')
		#valida la existencia de la ip
		elif conf_ini.es_IP_valida(ip):
			if (collection.find_one_and_delete({"ip" : str(ip)}) == None):
				print("\t\tLa Ip no existe en la BlackList.")
			else:
				descripcion = input("\tIntroduce una descripcion de por que desbloqueas esta Ip.\t\tVAWAF:>> ")
				print("\t\tLa Ip se desbloqueo correctamente.")
				ahora = datetime.datetime.now()
				collection_log.insert_one({"name":"desbloqueo","ip":ip,"descripcion":descripcion,"date_at":ahora})
				break
		else:
			print("\t\tLa Ip no tiene un formato válido.")

#desbloquear()