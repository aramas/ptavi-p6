#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

entrada = sys.argv

if len(entrada) != 3:
    print "Usage: python client.py method receiver@IP:SIPport"
    raise SystemExit
# Cliente UDP simple.

# Dirección IP del servidor.
METODO = entrada[1].upper()
SPLIT_PORT = entrada[2].split(":")
PORT = SPLIT_PORT[1]
SPLIT_NOMBRE = SPLIT_PORT[0].split("@")
NOMBRE = SPLIT_NOMBRE[0]
IP = SPLIT_NOMBRE[1]


# Contenido que vamos a enviar
LINE = METODO + " sip:" + SPLIT_PORT[0] + ' SIP/2.0\r\n\r\n'

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((IP, int(PORT)))
try:
        my_socket.send(LINE)
        data = my_socket.recv(1024)
        print "Enviando: " + LINE
except socket.error:
        print "Error: No server listening at " + IP + " port " + PORT
        raise SystemExit

print 'Recibido -- ', data

data_troz = data.split('\r\n\r\n')

if METODO == "INVITE" and data_troz[2] == 'SIP/2.0 200 OK':
        LINE = "ACK" + " sip:" + SPLIT_PORT[0] + ' SIP/2.0\r\n\r\n'
        print "Enviando: " + LINE
        my_socket.send(LINE)
        data = my_socket.recv(1024)


print "Terminando socket..."

# Cerramos todo
my_socket.close()
print "Fin."
