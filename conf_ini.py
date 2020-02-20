#!/usr/bin/env python
# -*- coding: utf-8 -*-
# By: José María HernAndez Estrada & Jason Adair Rossello Romero

import re
import getpass
from pymongo import MongoClient

# variables globales
Mongo_URI = 'mongodb://localhost'
client = MongoClient(Mongo_URI)


def es_correo_valido(correo):
    expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"

    return re.match(expresion_regular, correo) is not None


def es_IP_valida(ip):
    # ips = ip.replace(' ', '')
    return bool(re.match(r'^((0|[1-9][0-9]?|1[0-9][0-9]|2[0-4][0-9]|25[0-5])(\.|$)){4}$', ip))


def es_pass_valida(password):
    return bool(re.match(r'^(?=.*\d)(?=.*[\u0021-\u002b\u003c-\u0040])(?=.*[A-Z])(?=.*[a-z])\S{8,30}$', password))


def configuracionInicial():
    # presentaion al usuario
    print("**************** Bienvenido al VAWAF V1.0 ****************\n")
    print("Configuraciones iniciales:")

    # peticion de datos principales y validar
    while True:
        usuario = input("\tIngresa un nuevo usuario\t\t\tVAWAF:>> ")
        if len(usuario) <= 20 and len(usuario) >= 4:
            break
        else:
            print("\t\tUsuario invalido, usa máximo 20 caracteres y mínimo 4.")

    while True:
        password = getpass.getpass(prompt="\tIngresa una nueva contraseña\t\t\tVAWAF:>> ")
        if es_pass_valida(password):
            break
        else:
            print(
                "\t\tContraseña invalida, la contraseña debe tener al entre 8 y 30 caracteres, al menos un dígito, al menos una minúscula, al menos una mayúscula y al menos un caracter no alfanumérico..")

    while True:
        datos = input("\tIngresa IP:Puerto (1.1.1.1:8000)\t\tVAWAF:>> ")

        # tratado de datos ip/puerto
        dospuntos = datos.find(":")
        ip = ""
        puerto = ""
        if dospuntos > 0:
            datosSepados = datos.split(":")
            ip = datosSepados[0]
            puerto = datosSepados[1]
        # Valida la ip
        if (es_IP_valida(ip) and int(puerto) > 1023 and int(puerto) < 65536 and dospuntos > 0):
            break
        else:
            print("\t\tDirecion ip invalido o puerto invalido, intenta otra vez.")

    while True:
        email = input("\tIngresa un correo electrónico válido:\t\tVAWAF:>> ")
        if (es_correo_valido(email)):
            break
        else:
            print("\t\tCorreo invalido, intenta otra vez.")
    #	print(usuario, " - ", password, " - ", email, " - ", ip, " - ", puerto)

    # guardar los datos en mongo db
    db = client['waf']
    collection = db['config']
    un_dia = 1

    collection.insert_one({"name": "usuario", "valor": str(usuario)})
    collection.insert_one({"name": "password", "valor": str(password)})
    collection.insert_one({"name": "email", "valor": str(email)})
    collection.insert_one({"name": "puerto", "valor": str(puerto)})
    collection.insert_one({"name": "ip", "valor": str(ip)})
    # documentos precargados
    collection.insert_one({"name": "numataques", "valor": 500})
    collection.insert_one({"name": "cuarentena", "valor": un_dia})
    collection.insert_one({"name": "tiempobl", "valor": un_dia})

    print("\tDatos guardados exitosamente.")

    # impresion de los datos
    results = collection.find()
    for r in results:
        print("\t", r)

# if  __name__ ==  '__main__':
#	configuracionInicial()
