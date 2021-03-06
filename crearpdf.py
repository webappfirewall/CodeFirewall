from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def crear(sistema,comunidad,indice):
    global can
    can = canvas.Canvas("Reporte"+str(indice)+".pdf", pagesize=letter)
    can.setLineWidth(.3)
    can.setFont('Helvetica', 20)
    can.drawString(200, 750, 'Reporte de monitoreo SNMP')
    can.setFont('Helvetica', 12)
    can.drawString(30, 710, 'Paquetes multicast que ha recibido una interfaz: ')
    can.drawString(200, 740, str(sistema) + "    " + comunidad)
    # Dibujamos una imagen (IMAGEN, X,Y, WIDTH, HEIGH)
    can.drawImage('multicast.png',100,550, 397, 130)
    can.drawString(30, 480, 'Paquetes recibidos exitosamente, entregados a protocolos IPv4: ')
    # Dibujamos una imagen (IMAGEN, X,Y, WIDTH, HEIGH)
    can.drawImage('recibidos.png',100,310, 397, 130)
    can.drawString(30, 230, 'Mensajes de respuesta ICMP que ha enviado el agente: ')
    # Dibujamos una imagen (IMAGEN, X,Y, WIDTH, HEIGH)
    can.drawImage('respuestaicmp.png',100,60, 397, 130)
    # Salto de pagina
    can.showPage()
    can.drawString(30, 750, 'Segmentos enviados, incluyendo los de las conexiones actual pero excluyendo los que contienen solamente')
    can.drawString(30, 733, 'octetos retransmitidos:')
    # Dibujamos una imagen (IMAGEN, X,Y, WIDTH, HEIGH)
    can.drawImage('enviados.png',100,550, 397, 130)
    can.drawString(30, 500, 'Datagramas recibidos que no pudieron ser entregados por cuestiones distintas a la falta de aplicación ')
    can.drawString(30, 483, 'en el puerto destino: ')
    # Dibujamos una imagen (IMAGEN, X,Y, WIDTH, HEIGH)
    can.drawImage('datarecibidos.png',100,310, 397, 130)

    can.save()