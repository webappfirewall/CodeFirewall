#!/usr/bin/env python
# -*- coding: utf-8 -*-
# By: José María Hernández Estrada & Jason Adair Rossello Romero

import threading
import time
import urllib.parse
import correo
import main
import analizador
from pymongo import MongoClient
import conexiondb
import wafd

# Variables globales
client = conexiondb.client


def hcorreo():
    while True:
        correo.checa_envio()
        time.sleep(120) #cambiar a 300


def hwaf():
    db = client['waf']
    collection = db['trama']
    #corre infinitamente el analizador de patrones
    while True:
        time.sleep(5) #borrar el retardo
        if collection.count_documents({}) > 0:
            analizador.main()


def wafdaemon():
    wafd.initWAF()


def menu():
    print("\n**************** Firewall v1.0 ****************\n")
    print("1. Configuraciones.")
    print("2. Salir.")


def principal():
    #se crean los objetos hilo
    hiloCorreo = threading.Thread(name='HCorreo',target=hcorreo, daemon=True)
    wafService = threading.Thread(name='wafService', target=hwaf, daemon=True)
    wafd = threading.Thread(name='wafd', target=wafdaemon, daemon=True)
    hilomain = threading.Thread(name='HMain', target=main.primeraVez, daemon=False)
    banderaH = 0

    while True:
        # imprime el menu
        menu()
        opcion = input("\nVAWAF:>> ")

        if opcion == "1":
            # corre los hilos demonio
            if banderaH == 0:
                hiloCorreo.start()
                wafService.start()
                wafd.start()
                banderaH = 1
            main.primeraVez()
        elif opcion == "2" or opcion == 'exit' or opcion == 'EXIT':
            print("Good bye baby.")
            break
        else:
            print('Opcion invalida.')


principal()