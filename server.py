#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import SocketServer
import sys
import os

entrada = sys.argv
if len(entrada) != 4:
    print "Usage: python server.py IP port audio_file"
    raise SystemExit
IP = int(entrada[2])

class EchoHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        metodos = ["INVITE", "ACK", "BYE"]
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            split_line = line.split(" ")
            metodo = split_line[0]
            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break
            print "El cliente nos manda " + line
            if metodo == "INVITE":
                Mensaje = 'SIP/2.0 100 Trying\r\n\r\n'
		Mensaje += 'SIP/2.0 180 Ring\r\n\r\n'
                Mensaje += 'SIP/2.0 200 OK\r\n\r\n'
                print "Enviando: " + Mensaje
                self.wfile.write(Mensaje)
            elif metodo == "BYE":
                Mensaje = 'SIP/2.0 200 OK\r\n\r\n'
                print "Enviando: " + Mensaje
                self.wfile.write(Mensaje)
            elif metodo == "ACK":
                aEjecutar = './mp32rtp -i 127.0.0.1 -p 23032 < ' + entrada[3]
                os.system('chmod 755 mp32rtp')
                os.system(aEjecutar)
            elif metodo not in metodos:
                Mensaje = 'SIP/2.0 405 Method Not Allowed\r\n\r\n'
                self.wfile.write(Mensaje)
            else:
                Mensaje = 'SIP/2.0 400 Bad Request\r\n\r\n'
                self.wfile.write(Mensaje)

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = SocketServer.UDPServer(("", IP), EchoHandler)
    print "Listening..."
    serv.serve_forever()
