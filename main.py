#!/usr/bin/env python
# -*- coding: utf-8 -*-
# By: José María Hernández Estrada & Jason Adair Rossello Romero

import urllib.parse
import conf_ini
import cargar_bl
import cargar_wl
import desbloqueo
import modificaciones
import reporte
import getpass
from pymongo import MongoClient
import conexiondb

# Variables globales
client = conexiondb.client


def primeraVez():
    db = client['waf']

    collections = [db['config'], db['whitelist'], db['blacklist'], db['zonas']]
    if (collections[0].count_documents({}) == 0):
        conf_ini.configuracionInicial()
    else:
        login()


def login():
    db = client['waf']
    collection = db['config']

    while True:
        usuario = input("Ingresa el usuario:\t\tVAWAF:>>")
        usr = collection.find_one({'name':'usuario'})
        psw = collection.find_one({'name': 'password'})

        if usr['valor'] == usuario:
            print("\tUsuario Correcto.")
            break
        else:
            print("\tWARNING: El usuario ingresado es incorrecto.")

    while True:
        password = getpass.getpass("Ingresa la contraseña:\t\tVAWAF:>>")

        if psw['valor'] == password:
            print("Contraseña correcta.")
            main()
            break
        else:
            print("\tWARNING: La contraseña ingresada es incorrecta.")


def menu():
    print("\n**************** Firewall v1.0 ****************\n")
    print("1.  Cargar BlackList.")
    print("2.  Cargar WhiteList.")
    print("3.  Desbloqueo de IP.")
    print("4.  Generar reporte.")
    print("5.  Modificar Password.")
    print("6.  Modificar número de ataques para notificación.")
    print("7.  Modificar tiempo de cuarentena.")
    print("8.  Modificar tiempo de vaciado de BlackList.")
    print("9.  Modificar correo.")
    print("10. Salir (EXIT).\n")


def main():
    # valida si es la configuracion inicial
    #primeraVez()

    while (True):
        # imprime menu
        menu()
        # recibe opcion
        opcionMenu = input("VAWAF:>> ")
        # opciones
        if opcionMenu == "1":
            print(
                "_____________________________________________________________________________________________________________________\n")
            print("**** Cargar BlackList. ****\n")
            cargar_bl.cargar_bl()
            print("\nGuardado.")

        elif opcionMenu == "2":
            print(
                "_____________________________________________________________________________________________________________________\n")
            cargar_wl.cargarwl()
            print("\nGuardado.")

        elif opcionMenu == "3":
            print(
                "_____________________________________________________________________________________________________________________\n")
            print("**** Desbloquear IP. ****\n")
            desbloqueo.desbloquear()
            print("\nGuardado.")

        elif opcionMenu == "4":
            print(
                "_____________________________________________________________________________________________________________________\n")
            print("**** Generar reporte. ****\n\nGenerando...")
            try:
                reporte.generarReporte()
                print("Reporte generado exitosamente.\n")
            except ValueError:
                print("Ocurrio un error al generar el reporte.")

        elif opcionMenu == "5":
            print(
                "_____________________________________________________________________________________________________________________\n")
            print("**** Modificar Password. ****\n")
            modificaciones.mod_pass()
            print("\nGuardado.")

        elif opcionMenu == "6":
            print(
                "_____________________________________________________________________________________________________________________\n")
            print("**** Modificar número de ataques para notificación. ****\n")
            modificaciones.num_ataques()
            print("\nGuardado.")

        elif opcionMenu == "7":
            print(
                "_____________________________________________________________________________________________________________________\n")
            print("**** Modificar tiempo de cuarentena. ****\n")
            modificaciones.tcuarentena()
            print("\nGuardado.")

        elif opcionMenu == "8":
            print(
                "_____________________________________________________________________________________________________________________\n")
            print("**** Modificar tiempo de vaciado de BlackList. ****\n")
            modificaciones.vaciadobl()
            print("\nGuardado.")

        elif opcionMenu == "9":
            print(
                "_____________________________________________________________________________________________________________________\n")
            print("**** Modificar correo. ****\n")
            modificaciones.mod_correo()
            print("\nGuardado.")

        elif opcionMenu == "EXIT" or opcionMenu == "exit" or opcionMenu == "10":
            break

        else:
            print("")
            input("No has ingresado ningun comando correcto...\nPulsa una tecla para continuar.")
