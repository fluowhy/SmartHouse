# -*- coding: utf-8 -*-

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import time
import pyfirmata

# Este programa lee los pines analogico 0 y digital 2 de un arduino uno a traves
# del puerto USB y guarda un archivo de texto con la informacion del estado de 
# una luz ficticia representada por un LDR. Ademas muestra el voltaje digital
# promedio y analogico respectivos.

def estado(value):
	# determina el estado de una luz
	if value>0.5: # calcula el estado de la luz
		state = 'luz encendida'
	else:
		state = 'luz apagada'
	return state		

port = '/dev/ttyACM3' # puerto donde esta conectado el arduino (hay que cambiarlo dependiendo del pc)
board = pyfirmata.Arduino(port) # crea objeto como arduino en puerto anterior

it = pyfirmata.util.Iterator(board) # para que el buffer no haga overflow
it.start()

A0 = board.get_pin('a:0:i') # define pin analogico A0 como input
D2 = board.get_pin('d:2:i') # define pin digital D2 como input (ampolleta 1)
D3 = board.get_pin('d:3:i') # ampolleta 2
dt = 10 # tiempo de actualizacion en segundos
t1 = time.time() # toma tiempo inicial
while True:	
	t2 = time.time() # toma tiempo final
	dt = t2 - t1 # calcula dt
	if dt >= 10: # si dt > 10 segundos calcula estado de las luces
		k = 0 # muestras reales (hay problema con muestras None)
		a = 0 # guarda estado pin analogico (prueba)
		b = 0 # guarda estado pin digital
		c = 0
		for i in range(10): # el estado de las luces se calcula con un promedio de 10 muestras
			b1 = D2.read() # lee pin digital 2
			a1 = A0.read() # lee pin analogico 0 
			c1 = D3.read() # lee pin digital 3
			if a1!=None and b1!=None: # condicion para que no hayan NoneType
				k += 1
				a += a1
				b += b1
				c += c1
		if k!=0:
			print b/k # print valor digital
			print c/k
			print (5 - a/k*5)*2000/(a/k*5), 'Ohm' # print resistencia LDR	
			print a/k*5, 'V' # print voltaje en el divisor			
			State = np.array([[1, estado(b/k)], [2, estado(c/k)]]) # array a guardar (para usar con np.savetxt)
			np.savetxt('state', State, delimiter=" ", fmt="%s") # garda el txt actualizado
		t1 = time.time() # nuevo tiempo inicial
