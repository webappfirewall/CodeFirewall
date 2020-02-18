#!/usr/bin/env python
# -*- coding: utf-8 -*-
# By: José María Hernández Estrada & Jason Adair Rossello Romero

import datetime
from pymongo import MongoClient
from patrones import reservadas
from patrones import sql_keywords

# variables globales
client = MongoClient('127.0.0.1', 27017)


def analizador(datos):
    #convierte de ascci a caracter y guarada en la misma posicion de la lista
    for n in range(len(datos)):
        if datos[n][0] == '%':
            sincaracter = datos[n].replace('%', '')
            datos[n] = (b''.fromhex(sincaracter)).decode()
    print(datos)

    #busca los patrones
    for dato in datos:
        for keyword in sql_keywords:
            if dato == keyword:
                print("DANGER ESTO ES UN ATAQUE")

def extrae_datos(cadena):
    atributos = cadena.split('?')
    ruta_ext = atributos[0]
    parametros = atributos[1]

    datos_llaveValor = parametros.split('&')
    #print(datos_llaveValor)

    for llavev in datos_llaveValor:
        #separa por el igual
        datos = llavev.split('=')
        llave = datos[0]
        #separa por signos + la segunda parte
        valor = datos[1]
        informacion = valor.split('+')
        #print(informacion)
        analizador(informacion)

extrae_datos('/dvwa/vulnerabilities/sqli/?id=%27+or+1+%3D+%27+1&Submit=Submit')