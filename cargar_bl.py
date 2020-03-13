#!/usr/bin/env python
# -*- coding: utf-8 -*-
#By: José María HernAndez Estrada & Jason Adair Rossello Romero
import urllib.parse
import conf_ini
import datetime
import duplicidad_db
import muestraColecciones
from pymongo import MongoClient
import conexiondb

# Variables globales
client = conexiondb.client

def cargar_bl():
	db = client['waf']
	collections = [db['config'],db['whitelist'],db['blacklist'],db['zonas']]

	while True:
		ips = input("\tIngresa la IP separada por coma o por guion en caso de ser un rango.\tVAWAF:>> ")
		porcoma = ips.split(',')
		porguion = ips.split('-')

		#print(porguion)
		#print(porcoma)

#permite regresar con back
		if ips == "back" or ips == "BACK":
			break
#con el comando show muestra todas las ip contenidas en la base de datos
		elif ips == "show":
			muestraColecciones.showcoll('blacklist')
#es una unica ip
		elif (len(porguion) == 1 and len(porcoma) == 1):
			if (conf_ini.es_IP_valida(ips) and duplicidad_db.checar_duplicidad('blacklist', ips)):
				ahora = datetime.datetime.now()	#obtiene fecha y hora actual
				collections[2].insert_one({"ip":ips, "agent":"","ataque":"precargada", "date_at":ahora})
				#busca y borra en caso de estar en la wl
				duplicidad_db.buscaBorra(ips, 'whitelist')
				#print(ips)
				break
			else:
				if not(duplicidad_db.checar_duplicidad('blacklist', ips)):
					print("\tEsta Ip ya existe en la BlackList.")
				else:	
					print("\tIps introducidas incorrectamente...\nPulse una tecla para continuar.")

#estan separadas por comas
		elif (len(porguion) == 1 and len(porcoma) > 1):
			aux = []
			error = False
			print(porcoma)
			for x in porcoma:
				print(x)
				if (aux.count(x) < 1 and conf_ini.es_IP_valida(x)):
					aux.append(x)
				elif (aux.count(x) < 1 and conf_ini.es_IP_valida(x) == False):
					print("\tIps introducidas incorrectamente...coma1\nPulse una tecla para continuar.")
					error = True
					break
				elif (not(aux.count(x) < 1) and not(conf_ini.es_IP_valida(x))):
					print("\tIps introducidas incorrectamente...coma2\nPulse una tecla para continuar.")
					error = True
					break
			#ips validades sin errores, se procede a guardar en db
			if error == False:
				porcoma = aux
				if (conf_ini.es_IP_valida(porcoma[0]) and conf_ini.es_IP_valida(porcoma[1])):
					ahora = datetime.datetime.now() #obtiene fecha y hora actual
					for ip in porcoma:
						if(duplicidad_db.checar_duplicidad('blacklist', ip)):
							collections[2].insert_one({"ip":ip, "agent":"","ataque":"precargada", "date_at":ahora})
							# busca y borra en caso de estar en la wl
							duplicidad_db.buscaBorra(ip, 'whitelist')
						#print(ip)
					break

#estan separadas por guiones
		elif (len(porguion) > 1 and len(porcoma) == 1 and valida_rango((porguion[0].split('.')), (porguion[1]).split('.'))):
			if (conf_ini.es_IP_valida(porguion[0]) and conf_ini.es_IP_valida(porguion[1])):
				ahora = datetime.datetime.now() #obtiene echa y hora actual
				ip1 = porguion[0].split(".")
				ip2 = porguion[1].split(".")

				############quitaespacios

				#difieren en el ultimo tramo
				if (ip1[0] == ip2[0] and ip1[1] == ip2[1] and ip1[2] == ip2[2] and (ip1[3] > ip2[3] or ip1[3] < ip2[3])):
					rango = reloj(int(ip1[3]), int(ip2[3]))
					for i in rango:
						ipx = ip1[0] + "." + ip1[1] + "." + ip1[2] + "." + str(i)
						if(duplicidad_db.checar_duplicidad('blacklist', ipx)):
							collections[2].insert_one({"ip":ipx, "agent":"","ataque":"precargada", "date_at":ahora})
							# busca y borra en caso de estar en la wl
							duplicidad_db.buscaBorra(ipx, 'whitelist')
						#print(ipx)
					break

				#difieren en el 3er y 4to tramo 127.0.0.15-127.0.2.5
				elif (ip1[0] == ip2[0] and ip1[1] == ip2[1] and (ip1[2] < ip2[2] or ip1[2] > ip2[2]) and (ip1[3] > ip2[3] or ip1[3] < ip2[3] or ip1[3] == ip2[3])):
					tope = 256
					ipa = ip1
					control = ip1[3]
					ctl1 = int(ip2[2]) - int(ipa[2]) + 1
					ctl2 = int(ip2[2]) - int(ipa[2])

					for primero in range(ctl1):
						#comprueba ultima iteracion
						if (primero == ctl2):
							tope = int(ip2[3]) + 1
							#print ("\tEl tope es ",tope)
						for segundo in range(tope - int(control)):
							ipx = str(ip1[0]) + "." + str(ip1[1]) + "." + str(ip1[2]) + "." + str(ip1[3])
							if(duplicidad_db.checar_duplicidad('blacklist', ipx)):
								collections[2].insert_one({"ip":ipx, "agent":"","ataque":"precargada", "date_at":ahora})
								# busca y borra en caso de estar en la wl
								duplicidad_db.buscaBorra(ipx, 'whitelist')
							#print(ipx)
							ip1[3] = int(ip1[3]) + 1
						ip1[2] = int(ip1[2]) + 1
						ip1[3] = 0
						control = 0
					break
				elif (ip1[0] == ip2[0] and ip1[1] == ip2[1] and ip1[2] == ip2[2] and ip1[3] == ip2[3]):
					print("\t\t\tWARNING: Las Ips no pueden ser identicas.\n\t\t\tPulse una tecla para continuar.")
				else:
					print("\t\t\tWARNING: En caso de que exista variacion en el primer y segundo octeto ir a la configuraion por zonas, las Ip no pueden ser duplicadas.\n\t\t\tPulse una tecla para continuar.")
			else:
				print("\tIps introducidas incorrectamente...\nPulse una tecla para continuar.")
		#default
		else:
			print("\tIps introducidas incorrectamente, la primera Ip debe ser menor que la segunda Ip\n\t\t\tWARNING En caso de que exista variacion en el primer y segundo octeto ir a la configuraion por zonas...\nPulse una tecla para continuar.")

def valida_rango(ip1, ip2):#127.1.2.250-127.2.2.10
	if (int(ip1[0])<=int(ip2[0]) and int(ip1[1])<=int(ip2[1]) and int(ip1[2])<=int(ip2[2]) and int(ip1[3])<=int(ip2[3])):
		return True
	else:
		return False

def reloj(ip1, ip2):
	rango = []
	for i in range(int(ip2) - int(ip1) + 1):
		rango.append(int(ip1 + i))

	return rango

#cargar_bl()