#!/usr/bin/env python
# -*- coding: utf-8 -*-
#By: José María Hernández Estrada & Jason Adair Rossello Romero

import re
from pymongo import MongoClient

Mongo_URI = 'mongodb://52.254.64.58'

def es_correo_valido(correo):
    expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    
    return re.match(expresion_regular, correo) is not None
 
def es_IP_valida(ip):

    return bool(re.match(r'^((0|[1-9][0-9]?|1[0-9][0-9]|2[0-4][0-9]|25[0-5])(\.|$)){4}$', ip))

def es_pass_valida(password):

	 return bool(re.match(r'^(?=.*\d)(?=.*[\u0021-\u002b\u003c-\u0040])(?=.*[A-Z])(?=.*[a-z])\S{8,30}$',password))

def configuracionInicial():
	#presentaion al usuario
	print("**************** Bienvenido al VAWAF V1.0 ****************\n")
	print("Configuraciones iniciales:")

	#peticion de datos principales y validar
	while True:
		usuario 	= input("Ingresa un nuevo usuario				VAWAF:>> ")
		if len(usuario)<20:
			break
		else:
			print("Usuario invalido, usa máximo 20 caracteres.")

	while True:
		password 	= input("Ingresa una nueva contraseña			VAWAF:>> ")
		if es_pass_valida(password):
			break
		else:
			print("Contraseña invalida, la contraseña debe tener al entre 8 y 30 caracteres, al menos un dígito, al menos una minúscula, al menos una mayúscula y al menos un caracter no alfanumérico..")

	while True:
		datos 		= input("Ingresa IP:Puerto (1.1.1.1:8000)		VAWAF:>> ")
		
		#tratado de datos ip/puerto
		dospuntos = datos.find(":")
		ip = ""
		puerto = ""
		if dospuntos > 0:
			datosSepados = datos.split(":")
			ip = datosSepados[0]
			puerto = datosSepados[1]
		#Valida la ip
		if(es_IP_valida(ip) and int(puerto)>1023 and int(puerto)<65536 and dospuntos>0):
			break
		else:
			print("Direcion ip invalido o puerto invalido, intenta otra vez.")

	while True:
		email 		= input("Ingresa un correo electrónico válido:	VAWAF:>> ")
		if(es_correo_valido(email)):
			break
		else:
			print("Correo invalido, intenta otra vez.")
	
	print(usuario, " - ", password, " - ", email, " - ", ip, " - ", puerto)

	#guardar los datos en mongo db



def menu():
	print("**************** Firewall ****************")
	print(	"1.	")
	print(	"2.	")
	print(	"3.	")
	print(	"4.	")
	print(	"5.	")
	print(	"6.	")
	print(	"7.	")

if  __name__ ==  '__main__':

	configuracionInicial()

	while (True):
		#imprime menu
		menu()

		#recibe opcion
		opcionMenu = input("VAWAF:>> ")
		#opciones
		if opcionMenu == "1":
			print("")

		elif opcionMenu == "2":
			print("")

		elif opcionMenu == "EXIT":
			print("Good bye baby")
			break

		else:
			print ("")
			input("No has ingresado ningun comando correcto...\nPulsa una tecla para continuar")
