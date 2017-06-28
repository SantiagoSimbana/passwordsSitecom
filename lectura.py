#for n in range (0, ffff, hex):
#	print n

lista = ''
lista1 = []
lista2 = []
final = []

key = open('sitecom.txt', 'r')
diccionario = open('diccio4000.txt', 'r')

#print key

for linea in key:
	lista1.append(linea)
#	print lista1[0]
	
g = 0

for linea in diccionario:
	lista2.append(linea)
	x = lista2[g]
	x = x[:12] 
#	print x
	lista2[g] = x
#	lista2[g] = lista2[:12]
	g = g + 1
#	print lista2
#	elemento = elemento[:12]
#print lista2

#varia = 0
#print lista1
for i in lista1:
	if i in lista2:
		j = lista1[0]
#		print type(j)
		print "La clave es: %s" %j
		
	else:
		print 'No fue posible obtener la contrasena'
	
