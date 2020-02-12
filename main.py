#!/usr/bin/env python
# -*- coding: utf-8 -*-
#By: José María HernAndez Estrada & Jason Adair Rossello Romero

import re
import conf_ini
import cargar_bl
import cargar_wl
import desbloqueo
import modificaciones
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
	print(	"7.  Modificar número de ataques para notificación.")
	print(	"8.  Modificar tiempo de cuarentena.")
	print(	"9.  Modificar tiempo de vaciado de BlackList.")
	print(	"10. Modificar correo.")
	print(	"11. Salir (EXIT).\n")

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
			print("_____________________________________________________________________________________________________________________\n")
			print("**** Cargar BlackList. ****\n")
			cargar_bl.cargar_bl()
			print("\nGuardado.")

		elif opcionMenu == "2":
			print("_____________________________________________________________________________________________________________________\n")
			cargar_wl.cargarwl()
			print("\nGuardado.")

		elif opcionMenu == "3":
			print("_____________________________________________________________________________________________________________________\n")
			print("**** Desbloquear IP. ****\n")
			desbloqueo.desbloquear()
			print("\nGuardado.")

		elif opcionMenu == "4":
			print("_____________________________________________________________________________________________________________________\n")
			print("**** Generar reporte. ****\n")
			print("\nGuardado.")

		elif opcionMenu == "5":
			print("_____________________________________________________________________________________________________________________\n")
			print("**** Bloqueo por zona. ****\n")
			print("\nGuardado.")

		elif opcionMenu == "6":
			print("_____________________________________________________________________________________________________________________\n")
			print("**** Modificar Password. ****\n")
			modificaciones.mod_pass()
			print("\nGuardado.")

		elif opcionMenu == "7":
			print("_____________________________________________________________________________________________________________________\n")
			print("**** Modificar número de ataques para notificación. ****\n")
			modificaciones.num_ataques()
			print("\nGuardado.")

		elif opcionMenu == "8":
			print("_____________________________________________________________________________________________________________________\n")
			print("**** Modificar tiempo de cuarentena. ****\n")
			modificaciones.tcuarentena()
			print("\nGuardado.")

		elif opcionMenu == "9":
			print("_____________________________________________________________________________________________________________________\n")
			print("**** Modificar tiempo de vaciado de BlackList. ****\n")
			modificaciones.vaciadobl()
			print("\nGuardado.")

		elif opcionMenu == "10":
			print("_____________________________________________________________________________________________________________________\n")
			print("**** Modificar correo. ****\n")
			modificaciones.mod_correo()
			print("\nGuardado.")

		elif opcionMenu == "EXIT" or opcionMenu == "exit" or opcionMenu == "11":
			print("Good bye baby.")
			break

		else:
			print ("")
			input("No has ingresado ningun comando correcto...\nPulsa una tecla para continuar.")