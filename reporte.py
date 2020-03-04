#!/usr/bin/env python
# -*- coding: utf-8 -*-
# By: José María Hernández Estrada & Jason Adair Rossello Romero

import urllib.parse
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
username = urllib.parse.quote_plus('@dm1n')
passwor = urllib.parse.quote_plus('Qw3rt&12345')
client = MongoClient('mongodb://%s:%s@10.0.2.4' % (username, passwor))
db = client['waf']
collection = db['log']


def generarReporte():
    global canv
    y = 800
    canv = canvas.Canvas("ReporteWaf.pdf", pagesize=letter)
    canv.setLineWidth(.3)
    canv.setFont('Helvetica', 20)
    canv.drawString(200, 750, 'Reporte del sistema WAF')

#mandamos el valor actual de y, estas son las funciones para llamar los tramos que contienen ips
    y = 690
    y = tramosip(y, 'Ip precargadas en la WhiteList.', 'Ip: ', 'whitel')
    y = tramosip(y, 'Ips desbloqueadas manualmente.', 'Ip: ', 'desbloqueo')
# mandamos el valor actual de y, estas son las funciones para llamar los tramos que contienen configuraciones
    y = tramos(y, 'Modificaciones de contraseña.', 'Contraseña actualizada: ', 'password')
    y = tramos(y, 'Modificaciones de número de ataques para notificación.', 'Límite: ', 'numataques')
    y = tramos(y, 'Modificaciones de tiempo de cuarentena de una Ip.', 'Tiempo(dias): ', 'cuarentena')
    y = tramos(y, 'Modificaciones de tiempo de vaciado de la BlackList.', 'Tiempo(dias): ', 'tiempobl')
    tramos(y, 'Modificaciones de correo electrónico.', 'Tiempo(dias): ', 'email')

    canv.save()

def tramos(y, subtitulo, texto, llave):
    y = y - 10
    y = hojaNueva(y)
    canv.setFont('Helvetica', 12)
    canv.drawString(30, y, subtitulo)
    y = y - 20
    y = hojaNueva(y)
    if collection.find({'name': llave}) != None:
        passu = collection.find({'name': llave})
        for dato in passu:
            canv.setFont('Helvetica', 8)
            text =  texto + str(dato['valor']) + " - Fecha: " + str(dato['date_at'])
            if len(text) > 125:
                text, text2, y = lineaNueva(text, y)
                canv.drawString(50, y + 10, text2)
                canv.drawString(50, y, text)
            else:
                canv.drawString(50, y, text)
                y = y - 10
                y = hojaNueva(y)
    return y

def tramosip(y, subtitulo, texto, llave):
    y = y - 10
    y = hojaNueva(y)
    canv.setFont('Helvetica', 12)
    canv.drawString(30, y, subtitulo)
    y = y - 20
    y = hojaNueva(y)
    if collection.find({'name': llave}) != None:
        passu = collection.find({'name': llave})
        for dato in passu:
            canv.setFont('Helvetica', 8)
            text = texto + str(dato['ip']) + " - Descripción: " + dato['descripcion'] + " - Fecha: " + str(dato['date_at'])
            if len(text) > 125:
                text, text2, y = lineaNueva(text, y)
                canv.drawString(50, y+10, text2)
                canv.drawString(50, y, text)
                y -= 10
            else:
                canv.drawString(50, y, text)
                y = y - 10
                y = hojaNueva(y)
    return y

def hojaNueva(y):
    if y <= 30:
        # Salto de pagina
        canv.showPage()
        y = 750
        return y
    else:
        return y

def lineaNueva(texto,y):
    if len(texto) > 125:
        # Salto de linea
        y = y - 10
        aux = ""
        aux2 = ""
        for t in range(len(texto)):
            if t > 125:
                aux += str(texto[t])
            else:
                aux2 += str(texto[t])
        return aux, aux2, y
    else:
        return y

def prueba():
    global can
    can = canvas.Canvas("prueba.pdf", pagesize=letter)
    can.setLineWidth(.3)
    can.setFont('Helvetica', 8)

    can.drawString(50, 720,'12345612312111111111111111111111111111113333333333333333322222222222222333333223222222222222222222222222222222222222222222133')
    texto = '1234561231111111111111111111111111111112111111111111111111111111111113333333333333333322222222222222333333223222222222222222222222222222222222222222222133'
    y = 720
    texto,y = lineaNueva(texto, y)
    can.drawString(50, y, texto)
    can.save()

#generarReporte()
#prueba()
