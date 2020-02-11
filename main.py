#!/usr/bin/env python
# -*- coding: utf-8 -*-
#By: José María HernAndez Estrada & Jason Adair Rossello Romero

import re
import conf_ini
import cargar_bl
from pymongo import MongoClient

#variables globales
Mongo_URI = 'mongodb://localhost'
client = MongoClient(Mongo_URI)

def primeraVez():
	db = client['waf']

	collections = [db['configuraciones'],db['whitelist'],db['blacklist'],db['zonas']]
	if (collections[0].count_documents({}) == 0):
		conf_ini.configuracionInicial()
	else:
		login()

def login():
	pass

def menu():
	print("\n**************** Firewall ****************\n")
	print(	"1.  Cargar BlackList.")
	print(	"2.  Cargar WhiteList.")
	print(	"3.  Desbloqueo de IP.")
	print(	"4.  Generar reporte.")
	print(	"5.  Bloqueo por zona")
	print(	"6.  Modificar Password")
	print(	"7.  Modificar numero de ataques para notificacion.")
	print(	"8.  Modificar tiempo de cuarentena.")
	print(	"9.  Modificar tiempo de vaciado de BlackList.")
	print(	"11. Modificar correo.")
	print(	"12. Salir (EXIT).\n")

if  __name__ ==  '__main__':

#valida si es la configuracion inicial
	primeraVez()

	while (True):
		#imprime menu
		menu()

		#recibe opcion
		opcionMenu = input("VAWAF:>> ")
		#opciones
		if opcionMenu == "1":
			print("**** Cargar BlackList. ****")
			cargar_bl.cargar_bl()

		elif opcionMenu == "2":
			print("")

		elif opcionMenu == "EXIT" or opcionMenu == "exit" or opcionMenu == "12":
			print("Good bye baby.")
			break

		else:
			print ("")
			input("No has ingresado ningun comando correcto...\nPulsa una tecla para continuar.")