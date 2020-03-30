#!/usr/bin/env python
# -*- coding: utf-8 -*-
# By: José María Hernández Estrada & Jason Adair Rossello Romero

import urllib.parse
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib
import reporte
from pymongo import MongoClient
import conexiondb

# Variables globales
client = conexiondb.client
db = client['waf']

mailsender = "correowaf@gmail.com"
mailreceip = "chemahernandez013@gmail.com"
mailserver = 'smtp.gmail.com: 587'
password = 'Global.nix12345'
subject = 'Alerta Firewall, límite de ataques excedido.'


def send_alert():
    global mailreceip
    # extrae el correo de las configuraciones iniciales
    try:
        coll_conf = db['config']
        datosmail = coll_conf.find_one({'name': 'email'})
        mailreceip = datosmail['valor']
    except ValueError:
        print('Error al obtener el correo')

    # inicializa parametros
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = mailsender
    msg['To'] = mailreceip

    # adjunta el pdf
    part = MIMEApplication(open("ReporteWaf.pdf", "rb").read())
    part.add_header('Content-Disposition', 'attachment', filename="ReporteWaf.pdf")
    msg.attach(part)

    # establece comunicacion con el servidor de correo
    mserver = smtplib.SMTP(mailserver)
    mserver.starttls()
    # Login Credentials for sending the mail
    mserver.login(mailsender, password)
    # envia el correo
    mserver.sendmail(mailsender, mailreceip, msg.as_string())
    mserver.quit()
    # print("\n\n*****Correo enviado exitosamente.*****\n")


def checa_envio():
    try:
        coll_conf = db['config']
        if coll_conf.find_one({"name": "numataques"}) != None:
            nataques = coll_conf.find_one({"name": "numataques"})
            limEstablecido = nataques['valor']
        else:
            limEstablecido = 250
            coll_conf.insert_one({'name': 'limite', 'valor': 0})
        documento = coll_conf.find_one({'name': 'limite'})
        limite = documento['valor']

        # si escuentra el limite
        if int(limite) >= int(limEstablecido):
            # actualiza el reporte
            reporte.generarReporte()
            # envia la alerta
            send_alert()
            # borra el contador de ataques
            coll_conf.find_one_and_replace({'name': 'limite'}, {'name': 'limite', 'valor': '0'})
    except ValueError:
        print('Error al obtener los datos de limites de ataques.')

# checa_envio() #es la funcion principal
# coll_log = db['log']
# coll_log.find_one_and_replace({'name': 'limite'}, {'name': 'limite', 'valor': '50'})
