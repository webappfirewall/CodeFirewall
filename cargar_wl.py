#!/usr/bin/env python
# -*- coding: utf-8 -*-
#By: José María HernAndez Estrada & Jason Adair Rossello Romero

import urllib.parse
import conf_ini
import datetime
import muestraColecciones
import duplicidad_db
from pymongo import MongoClient

#variables globales
username = urllib.parse.quote_plus('@dm1n')
passwor = urllib.parse.quote_plus('Qw3rt&12345')
client = MongoClient('mongodb://%s:%s@10.0.2.4' % (username, passwor))

def menu():
	print("\n**** Cargar WhiteList. ****\n")
	print(	"1.  Cargar una Ip.")
	print(	"2.  Salir(EXIT).\n")

def cargarwl():
	db = client['waf']
	collections = [db['config'],db['whitelist'],db['blacklist']]
	collections_log = db['log']

	while True:
		menu()
		opcion = input("\tIngresa una opción.\t\tVAWAF:>> ")

		#permite regresar con back
		if opcion == "back" or opcion == "BACK":
			break
		# con el comando show muestra todas las ip contenidas en la base de datos
		elif opcion == "show":
			muestraColecciones.showcoll('whitelist')
		elif opcion == "1":
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
		#guarda en log lo mismo para reportar
			collections_log.insert_one({"name":"whitel","ip":ip,"descripcion":descripcion,"date_at":ahora})
			print("Ip guardada correctamente.")

		elif( opcion == "2" or opcion == "EXIT"):
			break

		else:
			print("Opcion invalida...\n Pulsar cualquier tecla para continuar.")

#cargarwl()