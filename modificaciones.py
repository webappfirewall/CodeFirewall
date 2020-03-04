#!/usr/bin/env python
# -*- coding: utf-8 -*-
# By: José María HernAndez Estrada & Jason Adair Rossello Romero

import urllib.parse
import conf_ini
import getpass
import datetime
from pymongo import MongoClient

# variables globales
username = urllib.parse.quote_plus('@dm1n')
passwor = urllib.parse.quote_plus('Qw3rt&12345')
client = MongoClient('mongodb://%s:%s@10.0.2.4' % (username, passwor))
db = client['waf']
collection = db['config']
collection_log = db['log']


def mod_pass():
    while True:
        passActual = getpass.getpass(prompt="\tIngrese su contraseña actual.\t\tVAWAF:>> ")

        # permite regresar con back
        if passActual == "back" or passActual == "BACK":
            break
        elif collection.find_one({"name": "password", "valor": passActual}) == None:
            print("\tLa contraseña es incorrecta.")
        else:
            print("\t\tContraseña correcta.")
            while True:
                nuevaPass = getpass.getpass(prompt="\tIngrese una contraseña nueva.\t\tVAWAF:>> ")
                # la contraseña debe ser diferente de la actual y debe ser la misma en la confirmacion
                if conf_ini.es_pass_valida(nuevaPass) and nuevaPass != passActual:
                    while True:
                        nuevaPassVerifi = getpass.getpass(prompt="\tIngrese nuevamente la contraseña.\tVAWAF:>> ")
                        # verifica que la confirmacion sea identica
                        if nuevaPass == nuevaPassVerifi:
                            # guardado de la nueva contraseña
                            collection.find_one_and_replace({"name": "password", "valor": passActual},
                                                            {"name": "password", "valor": nuevaPass})
                            # guarda en log para reportar
                            collection_log.insert_one(
                                {"name": "password", "valor": nuevaPass, "date_at": datetime.datetime.now()})
                            break
                        else:
                            print("\t\tWARNIG La contraseña no es la misma.")
                    break
                else:
                    if nuevaPass == passActual:
                        print("\t\tLa nueva contraseña no puede ser la misma que la actual.")
                    else:
                        print("\t\tLa nueva contraseña no tiene el formato adecuado.")
            # brak principal
            break


def num_ataques():
    while True:
        numero = input("\tIngrese el nuevo un número de ataques para notificación (entre 50 y 1000).\t\tVAWAF:>> ")

        try:
            numero = int(numero)
            # permite regresar con back
            if numero == "back" or numero == "BACK":
                break
            elif int(numero) >= 50 and int(numero) <= 1000:
                # busca y reemplaza el valor
                collection.find_one_and_replace({"name": "numataques"}, {"name": "numataques", "valor": int(numero)})
                # guarda en log para reportar
                collection_log.insert_one(
                    {"name": "numataques", "valor": int(numero), "date_at": datetime.datetime.now()})
                break
            else:
                print("Número inválido, debe estar en número y entre 50 y 1000")
        except ValueError:
            print("Tiempo inválido, debe ser un número y  estar entre 1 y 29")


def tcuarentena():
    while True:
        numero = input("\tIngrese el nuevo tiempo de cuarentena en dias (entre 1 y 29).\t\tVAWAF:>> ")

        try:
            numero = int(numero)
            # permite regresar con back
            if numero == "back" or numero == "BACK":
                break
            elif int(numero) >= 1 and int(numero) <= 29:
                # busca y reemplaza los datos
                collection.find_one_and_replace({"name": "cuarentena"}, {"name": "cuarentena", "valor": int(numero)})
                # guarda en log para reportar
                collection_log.insert_one(
                    {"name": "cuarentena", "valor": int(numero), "date_at": datetime.datetime.now()})
                break
            else:
                print("Tiempo inválido, debe ser un número y  estar entre 1 y 29")
        except ValueError:
            print("Tiempo inválido, debe ser un número y  estar entre 1 y 29")


def vaciadobl():
    while True:
        numero = input("\tIngrese el nuevo tiempo de vaciado de la BlackList en días (entre 1 y 100).\t\tVAWAF:>> ")

        try:
            numero = int(numero)
            # permite regresar con back
            if numero == "back" or numero == "BACK":
                break
            elif int(numero) >= 1 and int(numero) <= 100:
                collection.find_one_and_replace({"name": "tiempobl"}, {"name": "tiempobl", "valor": int(numero)})
                # guarda en log para reportar
                collection_log.insert_one(
                    {"name": "tiempobl", "valor": int(numero), "date_at": datetime.datetime.now()})
                break
            else:
                print("Tiempo inválido, debe ser un número y  estar entre 1 y 100")
        except ValueError:
            print("Tiempo inválido, debe ser un número y  estar entre 1 y 29")


def mod_correo():
    while True:
        correo = input("\tIngrese el nuevo correo.\t\tVAWAF:>> ")

        # permite regresar con back
        if correo == "back" or correo == "BACK":
            break
        elif (conf_ini.es_correo_valido(correo)):
            collection.find_one_and_replace({"name": "email"}, {"name": "email", "valor": correo})
            # guarda en log para reportar
            collection_log.insert_one({"name": "email", "valor": correo, "date_at": datetime.datetime.now()})
            break
        else:
            print("\tEl formato del correo no es correto.")

# mod_pass()
# num_ataques()
# prueba()
