#!/usr/bin/env python
# -*- coding: utf-8 -*-
#By: José María HernAndez Estrada & Jason Adair Rossello Romero

import conf_ini
import datetime
import calendar
import duplicidad_db
from pymongo import MongoClient

#variables globales
client = MongoClient('127.0.0.1', 27017)

def menu():
	print("\n**** Cargar WhiteList. ****\n")
	print(	"1.  Cargar una Ip.")
	print(	"2.  Salir(EXIT).\n")

def cargarwl():
	db = client['waf']
	collections = [db['config'],db['whitelist'],db['blacklist'],db['zonas']]

	while True:
		menu()
		opcion = input("\tIngresa una opción.\t\tVAWAF:>> ")

		if opcion == "1":
			while True:
				ip = input("\tIngresa una IP válida.\t\tVAWAF:>> ")
				if (conf_ini.es_IP_valida(ip) and duplicidad_db.checar_duplicidad('whitelist',ip) and duplicidad_db.esta_en_bl(ip)):
					print("\t\tIp válida.")
					break
				else:
					#checa si la ip esta presente en la blacklist
					if not(duplicidad_db.esta_en_bl(ip)):
						print("\t\tWARNING Esta Ip esta guardada en la BlackList.")
					else:
						print("\t\tWARNING Ip no válida o duplicada.")
		#pide la descripcion
			descripcion = input("\tIngresa una descripcion.\t\tVAWAF:>> ")

			ahora = datetime.datetime.now()
			collections[1].insert_one({"ip":ip, "descripcion":descripcion, "date_at":ahora})
			print("Ip guardada correctamente.")

		elif( opcion == "2" or opcion == "EXIT"):
			break

		else:
			print("Opcion invalida...\n Pulsar cualquier tecla para continuar.")

#cargarwl()