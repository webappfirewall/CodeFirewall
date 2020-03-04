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

# Variables globales
username = urllib.parse.quote_plus('@dm1n')
passwor = urllib.parse.quote_plus('Qw3rt&.12345')
client = MongoClient('mongodb://%s:%s@10.0.2.4' % (username, passwor))


def hcorreo():
    while True:
        correo.checa_envio()
        time.sleep(120) #cambiar a 300


def hwaf():
    db = client['waf']
    collection = db['trama']
    while True:
        time.sleep(5) #borrar el retardo
        if collection.count_documents({}) > 0:
            analizador.main()


def menu():
    print("\n**************** Firewall v1.0 ****************\n")
    print("1. Configuraciones.")
    print("2. Salir.")


def principal():
    #se crean los objetos hilo
    hiloCorreo = threading.Thread(name='HCorreo',target=hcorreo, daemon=True)
    wafService = threading.Thread(name='wafService', target=hwaf, daemon=True)
    hilomain = threading.Thread(name='HMain', target=main.primeraVez, daemon=False)

    while True:
        #imprime el menu
        menu()
        opcion = input("\nVAWAF:>> ")

        if opcion == "1":
            main.primeraVez()
            # corre los hilos demonio
            hiloCorreo.start()
            wafService.start()
        elif opcion == "2" or opcion == 'exit' or opcion == 'EXIT':
            break
        else:
            print('Opcion invalida.')


principal()
