#!/usr/bin/env python
# -*- coding: utf-8 -*-
# By: José María Hernández Estrada & Jason Adair Rossello Romero

from pymongo import MongoClient
from patrones import sql_keywords
from patrones import *

# variables globales
client = MongoClient('127.0.0.1', 27017)
db = client['waf']

def extrae_trama():  # extrae la trama de la base de datos en mongo y la ip y las retorna
    collection = db['trama']
    if collection.count_documents({}) == 1:
        datos = collection.find({'name': 'trama'})
        trama = datos[0]['valor']
        ip = datos[0]['ip']
        return trama, ip


def extrae_datos(cadena):
    atributos = cadena.split('?')
    ruta_ext = atributos[0]
    parametros = atributos[1]

    datos_llaveValor = parametros.split('&')
    # print(datos_llaveValor)

    for llavev in datos_llaveValor:
        # separa por el igual
        datos = llavev.split('=')
        llave = datos[0]
        # separa por signos + la segunda parte
        valor = datos[1]
        informacion = valor.split('+')
        # print(informacion)
        return informacion


def buscaenblack(ip):
    collection = db['blacklist']
    if (collection.find_one({"ip" : str(ip)}) == None):
        #no esta en la black
        return False
    else:
        #esta en la black
        print("Esta ip esta en la blacklist: " + ip)
        return True


def analizador(datos):
    # convierte de ascci a caracter y guarada en la misma posicion de la lista
    tramastring = ""
    for n in range(len(datos)):
        if datos[n][0] == '%':
            sincaracter = datos[n].replace('%', '')
            datos[n] = (b''.fromhex(sincaracter)).decode()
            tramastring = tramastring + str((b''.fromhex(sincaracter)).decode()) + " "
        else:
            tramastring = tramastring + str(datos[n]) + " "
    tramastring = tramastring.rstrip()
    print(tramastring)

    # busca los patrones
    for dato in datos:
        for keyword in sql_keywords:
            if dato == keyword:
                print("DANGER ESTO ES UN ATAQUE")


def main():
    trama,ip = extrae_trama()
    # la ip esta en la black y debe ser bloqueada
    if (buscaenblack(ip)):
        collection = db['trama']
        collection.find_one_and_replace({'name':'trama'}, {'name' : 'trama', 'ip' : ip, 'valor' : trama, 'veredicto' : '1'})
    #la ip no esta en la black list y se debe ejecutar el analizador de patrones
    else:
        datos_separados = extrae_datos(trama)
        analizador(datos_separados)

main()
# extrae_datos('/dvwa/vulnerabilities/sqli/?id=%27+or+1+%3D+%27+1&Submit=Submit')