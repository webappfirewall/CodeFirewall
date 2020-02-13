#!/usr/bin/env python
# -*- coding: utf-8 -*-
# By: José María Hernández Estrada & Jason Adair Rossello Romero

import conf_ini
import datetime
from pymongo import MongoClient
import reportlab
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# variables globales
client = MongoClient('127.0.0.1', 27017)
db = client['waf']
collection = db['log']


def generarReporte():
    global canv
    y = 800
    canv = canvas.Canvas("ReporteWaf.pdf", pagesize=letter)
    canv.setLineWidth(.3)
    canv.setFont('Helvetica', 20)
    canv.drawString(200, 750, 'Reporte del sistema WAF')

    y = 690
    canv.setFont('Helvetica', 12)
    canv.drawString(30, 710, 'Ip precargadas en la WhiteList.')
    canv.setFont('Helvetica', 8)
    if collection.find({'name': 'whitel'}) != None:
        cargaWhite = collection.find({'name':'whitel'})
        for dato in cargaWhite:
            canv.drawString(50 ,y , "Ip: " + dato['ip'] + " - Descripción: " + dato['descripcion'] + " - Fecha: " + str(dato['date_at']))
            y = y - 10

    y = tramos(y, 'Modificaciones de contraseña.', 'Contraseña actualizada: ', 'password')
    y = tramos(y, 'Modificaciones de número de ataques para notificación.', 'Límite: ', 'numataques')
    y = tramos(y, 'Modificaciones de tiempo de cuarentena de una Ip.', 'Tiempo(dias): ', 'cuarentena')
    y = tramos(y, 'Modificaciones de tiempo de vaciado de la BlackList.', 'Tiempo(dias): ', 'tiempobl')
    y = tramos(y, 'Modificaciones de correo electrónico.', 'Tiempo(dias): ', 'email')

    canv.save()

def tramos(y, subtitulo, texto, llave):
    y = y - 10
    canv.setFont('Helvetica', 12)
    canv.drawString(30, y, subtitulo)
    canv.setFont('Helvetica', 8)
    y = y - 20
    if collection.find({'name': llave}) != None:
        passu = collection.find({'name': llave})
        for dato in passu:
            canv.drawString(50, y, texto + str(dato['valor']) + " - Fecha: " + str(dato['date_at']))
            y = y - 10
    return y

def crear(sistema, comunidad, indice):
    global can
    can = canvas.Canvas("Reporte" + str(indice) + ".pdf", pagesize=letter)
    can.setLineWidth(.3)
    can.setFont('Helvetica', 20)
    can.drawString(200, 750, 'Reporte de monitoreo SNMP')
    can.setFont('Helvetica', 12)
    can.drawString(30, 710, 'Paquetes multicast que ha recibido una interfaz: ')
    can.drawString(200, 740, str(sistema) + "    " + comunidad)
    # Dibujamos una imagen (IMAGEN, X,Y, WIDTH, HEIGH)
    can.drawImage('multicast.png', 100, 550, 397, 130)
    can.drawString(30, 480, 'Paquetes recibidos exitosamente, entregados a protocolos IPv4: ')
    # Dibujamos una imagen (IMAGEN, X,Y, WIDTH, HEIGH)
    can.drawImage('recibidos.png', 100, 310, 397, 130)
    can.drawString(30, 230, 'Mensajes de respuesta ICMP que ha enviado el agente: ')
    # Dibujamos una imagen (IMAGEN, X,Y, WIDTH, HEIGH)
    can.drawImage('respuestaicmp.png', 100, 60, 397, 130)
    # Salto de pagina
    can.showPage()
    can.drawString(30, 750,
                   'Segmentos enviados, incluyendo los de las conexiones actual pero excluyendo los que contienen solamente')
    can.drawString(30, 733, 'octetos retransmitidos:')
    # Dibujamos una imagen (IMAGEN, X,Y, WIDTH, HEIGH)
    can.drawImage('enviados.png', 100, 550, 397, 130)
    can.drawString(30, 500,
                   'Datagramas recibidos que no pudieron ser entregados por cuestiones distintas a la falta de aplicación ')
    can.drawString(30, 483, 'en el puerto destino: ')
    # Dibujamos una imagen (IMAGEN, X,Y, WIDTH, HEIGH)
    can.drawImage('datarecibidos.png', 100, 310, 397, 130)

    can.save()


def extraeIpDesbl():
    cargaWhite = collection.find({'name': 'whitel'})
    ipdesbl = collection.find({'name': 'desbloqueo'})
    uppass = collection.find({'name': 'password'})
    numataques = collection.find({'name': 'numataques'})
    cuarentena = collection.find({'name': 'cuarentena'})
    tiempobl = collection.find({'name': 'tiempobl'})
    email = collection.find({'name': 'email'})

    for n in ipdesbl:
        print("desbl", n)


    for n in cargaWhite:
        print("white", n)
        print(n['ip'])

#extraeIpDesbl()
generarReporte()
