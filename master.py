#!/usr/bin/env python
# -*- coding: utf-8 -*-
# By: José María Hernández Estrada & Jason Adair Rossello Romero

import threading
import time
import correo
import main


def hcorreo():
    while True:
        correo.checa_envio()
        time.sleep(120)


def menu():
    print("\n**************** Firewall v1.0 ****************\n")
    print("1. Configuraciones.")
    print("2. Salir.")


def principal():
    hiloCorreo = threading.Thread(name='HCorreo',target=hcorreo, daemon=True)
    hilomain = threading.Thread(name='HMain', target=main.main, daemon=False)

    # corre el hilo dmonio de correo
    hiloCorreo.start()

    while True:
        #imprime el menu
        menu()
        opcion = input("\nVAWAF:>> ")

        if opcion == "1":
            hilomain.start()
            hilomain.join()
        elif opcion == "2" or opcion == 'exit' or opcion == 'EXIT':
            break
        else:
            print('Opcion invalida.')


principal()
