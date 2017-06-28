#SCRIPT TESIS

#importo librerias

import argparse
import os
import logging
import sys

#Defino los diccionarios que se utilizara para ambos modelos

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

#defino una funcion para crear un archivo de texto

def creaciontxt():

# abro un archivo llamado diccio en modo escritura

    archi=open('diccio.txt','w')

#cierro el archivo, es decir, aun no se crea el archivo
#solo tengo la funcion para crear dicho archivo

    archi.close()

# llamo a la funcion antes definida y dicho archivo se crea

creaciontxt()

#16777215 es el numero de elementos del diccionario

#16777215

#uso menos elementos para probar

num = 16777215
d = 0

#aqui se solicita el ingreso del numero del modelo
#y en caso de ingresar un numero de modelo errado
#se seguira mostrando la opcion de ingresar el modelo

while d == 0:
	model = int(raw_input("ingrese el modelo: "))
	if model == 4000:
		d = d +1

#con continue se hace que se salte todo lo demas
#y se siga con las lineas de codigo fuera de while
		
		continue
	elif model == 4004:
		d = d + 1
		continue
	else:
		print "Modelo seleccionado es incorrecto"

charset1, charset2 = CHARSETS[str(model)]

#todos los equipos SITECOM, segun el estandar OUI,
#empiezan con 64-D1-A3, pero el algoritmo usa solo "A3"

s = 'a3'

#el 16 indica que es un hexadecimal, y que lo paso a decimal
#a este decimal le pongo en binario cuyo formato sera de 8 bits
# de ahi el 8 y la b  

y = "{0:08b}".format(int(s, 16))

#2551334231
magic1 = 0x98124557
#274970
magic2 = 0x0004321a
#2147483648
magic3 = 0x80000000

#este lazo for ira desde 0 hasta el numero que se definio antes

for n in range(0, num):
#cada numero se pasa al formato binario, pero esta vez como
#ya es decimal no lo trnasformo y lo paso a un numero binario de 
#24 bits. Esto ya que los 6 caracteres hexadecimales despues del
#OUI corresponden a 24 bits
#al igual que 'a3' correspondia a 8 bits
	n = "{0:024b}".format(n)
#sumo la cadena anterios a3 a la nueva cadena y obtengo un total de 32 bits
	t = y + n
#como esta en binario ahora le paso a entero, por eso indico el '2', para que se
#sepa que de binario lo paso a entero
	t = int(t, 2)
	
	offsets = []

	for i in range(12):
		if (t & 0x1) == 0:
			t = t ^ magic2
			t = t >> 1
		else:
			t = t ^ magic1
			t = t >> 1
			t = t | magic3

		offset = t % len(charset1)

		offsets.append(offset)
	
	wpakey = ""
	wpakey += charset1[offsets[0]]

	for j in range(0, 11):
		magic5 = offsets[j]
		magic6 = offsets[j+1]

		if magic5 != magic6:
			magic5 = charset1[magic6]
		else:
			magic5 = (magic5 + j) % len(charset1)
			magic5 = charset2[magic5]
            
		wpakey += magic5


	archivo_salida = open("diccio.txt", "a")
#	for m in range(0, num):
	archivo_salida.write("%s\n" %wpakey)
	archivo_salida.close()

#for n in range (0, ffff, hex):
#	print n

#lista = ''
#lista1 = []
#lista2 = []
#final = []

#key = open('sitecom.txt', 'r')
#diccionario = open('diccio.txt', 'r')

#print key

#for linea in key:
#	lista1.append(linea)
#	print lista1[0]
	
#g = 0

#for linea in diccionario:
#	lista2.append(linea)
#	x = lista2[g]
#	x = x[:12] 
#	print x
#	lista2[g] = x
#	lista2[g] = lista2[:12]
#	g = g + 1
#	print lista2
#	elemento = elemento[:12]
#print lista2

#varia = 0

#for i in lista1:
#	if i in lista2:
#		j = lista1[0]
#		print type(j)
#		print "La clave es: %s" %j
		
#	else:
#		print 'No fue posible obtener la contrasena'
#	