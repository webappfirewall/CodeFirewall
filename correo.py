#!/usr/bin/env python
# -*- coding: utf-8 -*-
# By: José María Hernández Estrada & Jason Adair Rossello Romero

import urllib.parse
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib
import reporte
from pymongo import MongoClient

# variables globales
username = urllib.parse.quote_plus('@dm1n')
passwor = urllib.parse.quote_plus('Qw3rt&12345')
client = MongoClient('mongodb://%s:%s@10.0.2.4' % (username, passwor))
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
        collection = db['log']
        coll_cong = db['config']
        if coll_cong.find_one({"name": "numataques"}) != None:
            nataques = coll_cong.find_one({"name": "numataques"})
            limEstablecido = nataques['valor']
        else:
            limEstablecido = 250
        documento = collection.find_one({'name': 'limite'})
        limite = documento['valor']

        # si escuentra el limite
        if int(limite) >= int(limEstablecido):
            # actualiza el reporte
            reporte.generarReporte()
            # envia la alerta
            send_alert()
            # borra el contador de ataques
            collection.find_one_and_replace({'name': 'limite'}, {'name': 'limite', 'valor': '0'})
    except ValueError:
        print('Error al obtener los datos de limites de ataques.')


# checa_envio() #es la funcion principal
# coll_log = db['log']
# coll_log.find_one_and_replace({'name': 'limite'}, {'name': 'limite', 'valor': '50'})
