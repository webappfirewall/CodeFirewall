#!/usr/bin/env python
# -*- coding: utf-8 -*-
# By: José María Hernández Estrada & Jason Adair Rossello Romero

import conf_ini
import duplicidad_db
import patrones
import datetime
import concurrent.futures
import conexiondb

# Variables globales
client = conexiondb.client
db = client['waf']


def extrae_trama():  # extrae la trama de la base de datos en mongo y la ip y las retorna
    try:
        collection = db['trama']
        if collection.count_documents({}) == 1:
            datos = collection.find({'name': 'trama'})
            trama = datos[0]['valor']
            ip = datos[0]['ip']
            return trama, ip
    except ValueError:
        print("WARNING: Error en extraccion de trama.")


def extrae_datos(cadena, tipo):
    try:
        # trama de tipo get '/dvwa/vulnerabilities/sqli/?id=%27+or+1+%3D+%27+1&Submit=Submit'
        if tipo == "get":
            informacion = []
            atributos = cadena.split('?')
            ruta_ext = atributos[0]
            parametros = atributos[1]
            datos_llaveValor = parametros.split('&')
            # print(datos_llaveValor)

            for llavev in datos_llaveValor:
                # separa por el igual
                datos = llavev.split('=')
                informacion.append(datos[1])
            return informacion
        # trama de tipo post: 'username=%27admin+%40%C3%B1&password=admin&Login=Login'
        elif tipo == "post":
            informacion = []
            atributos = cadena.split('&')
            for i in atributos:
                valor = i.split('=')
                informacion.append(valor[1])
            return informacion
        else:
            print("Error en adquisición de datos.")
    except ValueError:
        print("WARNING: Error en adquisicion de datos.")


def enClaro(datos):
    try:
        # convierte de ascci a caracter y guarada en la misma posicion de la lista
        tramastring = ""
        bandera = 0
        contador = 0

        for i in range(len(datos)):
            if datos[i] == '%':
                caracterEspecial = datos[i + 1] + datos[i + 2]
                tramastring = tramastring + str((b''.fromhex(caracterEspecial)).decode())
                bandera = 1
            elif datos[i] == '+':
                tramastring = tramastring + " "
            elif contador >= 1:
                bandera = 0
                contador = 0
            elif bandera == 1:
                contador = contador + 1
            else:
                tramastring = tramastring + datos[i]
        return tramastring
    except ValueError:
        print("WARNING: Error al pasar en claro la trama.")


def buscaenblack(ip):
    collection = db['blacklist']
    if (collection.find_one({"ip": str(ip)}) == None):
        # no esta en la black
        return False
    else:
        # esta en la black
        print("Esta ip esta en la blacklist: " + ip)
        return True


def analizador(datos):
    # convierte de ascci a caracter y guarada en la misma posicion de la lista
    tramastring = enClaro(datos)

    # busca los patrones por medio de hilos y se guardan en una lista
    resultados = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(patrones.sql1, tramastring)
        return_value = future.result()
        resultados.append(return_value)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(patrones.sql2, tramastring)
        return_value = future.result()
        resultados.append(return_value)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(patrones.sql3, tramastring)
        return_value = future.result()
        resultados.append(return_value)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(patrones.sql4, tramastring)
        return_value = future.result()
        resultados.append(return_value)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(patrones.sql5, tramastring)
        return_value = future.result()
        resultados.append(return_value)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(patrones.sql6, tramastring)
        return_value = future.result()
        resultados.append(return_value)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(patrones.sql7, tramastring)
        return_value = future.result()
        resultados.append(return_value)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(patrones.sql8, tramastring)
        return_value = future.result()
        resultados.append(return_value)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(patrones.sql9, tramastring)
        return_value = future.result()
        resultados.append(return_value)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(patrones.sql10, tramastring)
        return_value = future.result()
        resultados.append(return_value)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(patrones.sql11, tramastring)
        return_value = future.result()
        resultados.append(return_value)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(patrones.sql12, tramastring)
        return_value = future.result()
        resultados.append(return_value)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(patrones.sql13, tramastring)
        return_value = future.result()
        resultados.append(return_value)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(patrones.sql14, tramastring)
        return_value = future.result()
        resultados.append(return_value)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(patrones.sql15, tramastring)
        return_value = future.result()
        resultados.append(return_value)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(patrones.sql16, tramastring)
        return_value = future.result()
        resultados.append(return_value)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(patrones.sql17, tramastring)
        return_value = future.result()
        resultados.append(return_value)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(patrones.sql18, tramastring)
        return_value = future.result()
        resultados.append(return_value)

    # print(resultados)
    return resultados


def guardaBlack(ips, agente):
    collection = db['blacklist']

    if (conf_ini.es_IP_valida(ips) and duplicidad_db.checar_duplicidad('blacklist', ips)):
        ahora = datetime.datetime.now()  # obtiene fecha y hora actual
        collection.insert_one({"ip": ips, "agent": str(agente), "ataque": "detectado", "date_at": ahora})
        # busca y borra en caso de estar en la wl
        duplicidad_db.buscaBorra(ips, 'whitelist')


def cuentataques():
    # esta funcion aumenta el contador de ataques en la coleccion log en una unidad, al encontrar un ataque
    collection = db['config']
    documento = collection.find_one({'name': 'limite'})
    limite = int(documento['valor']) + 1
    collection.find_one_and_replace({'name': 'limite'}, {'name': 'limite', 'valor': limite})


def main():
    flag = "0"
    trama, ip = extrae_trama()
    collection = db['trama']
    # la ip no esta analizada
    colecion = collection.find_one({'name': 'trama'})
    status = colecion['analizado']
    if (status == 'False'):
        # la ip esta en la black y debe ser bloqueada
        if (buscaenblack(ip)):
            documento = collection.find_one({'name': 'trama'})
            tipo = documento['tipo']
            collection.find_one_and_replace({'name': 'trama'},
                                            {'name': 'trama', 'ip': ip, 'valor': trama, 'veredicto': '1', 'tipo': tipo,
                                             'analizado': 'True'})
        # la ip no esta en la black list y se debe ejecutar el analizador de patrones
        else:
            documento = collection.find_one({'name': 'trama'})
            tipo = documento['tipo']
            # obtiene todos los valores de la llave valor separados por un &
            datos_separados = extrae_datos(trama, tipo)
            # itera por input y los manda al analizador
            for tram in datos_separados:
                resultados = analizador(enClaro(tram))
                for r in resultados:
                    if r == True and flag == "0":
                        collection = db['trama']
                        # extrae el agente y lo manda a la funcion guardar en la blacklist
                        try:
                            agente = collection.find_one({'name': 'trama'})['agent']
                        except ValueError:
                            agente = "No especifícado."
                        guardaBlack(ip, agente)
                        cuentataques()
                        collection.find_one_and_replace({'name': 'trama'},
                                                        {'name': 'trama', 'ip': ip, 'valor': trama, 'veredicto': '1',
                                                         'tipo': tipo, 'analizado': 'True'})
                        flag = "1"
            # bandera para cuando no tiene ataques, y modificar el analizado a True
            if flag == "0":
                collection = db['trama']
                collection.find_one_and_replace({'name': 'trama'},
                                                {'name': 'trama', 'ip': ip, 'valor': trama, 'veredicto': '0',
                                                 'tipo': tipo, 'analizado': 'True'})

# main()
# cuentataques()
# perro = extrae_datos('username=%27admin+%40%3D&password=admin&Login=Login','post')
# perro = extrae_datos('/dvwa/vulnerabilities/sqli/?id=%27+or+1+%3D+%27+1&Submit=Submit', 'get')
# print(perro)
# enClaro(perro[0])
# enClaro(perro[1])
# extrae_datos('/dvwa/vulnerabilities/sqli/?id=%27+or+1+%3D+%27+1&Submit=Submit')
