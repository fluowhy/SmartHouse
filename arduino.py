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

port = '/dev/ttyACM3' # puerto donde esta conectado el arduino (hay que cambiarlo dependiendo del pc)
board = pyfirmata.Arduino(port) # crea objeto como arduino en puerto anterior

it = pyfirmata.util.Iterator(board) # para que el buffer no haga overflow
it.start()

A0 = board.get_pin('a:0:i') # define pin analogico A0 como input
D2 = board.get_pin('d:2:i') # define pin digital D2 como input
dt = 10 # tiempo de actualizacion en segundos
t1 = time.time() # toma tiempo inicial
while True:	
	t2 = time.time() # toma tiempo final
	dt = t2 - t1 # calcula dt
	if dt >= 10: # si dt > 10 segundos calcula estado de las luces
		k = 0 # muestras reales (hay problema con muestras None)
		a = 0 # guarda estado pin analogico (prueba)
		b = 0 # guarda estado pin digital
		for i in range(10): # el estado de las luces se calcula con un promedio de 10 muestras
			a1 = D2.read() # lee el pin anaogico 
			b1 = A0.read() # lee pin digital 
			if a1!=None and b1!=None: # condicion para que no hayan NoneType
				k += 1
				a += a1
				b += b1
		if k!=0:
			print a/k # print vaor digital
			print (5 - b/k*5)*2000/(b/k*5), 'Ohm' # print resistencia LDR	
			print b/k*5, 'V' # print voltaje en el divisor
			if a/k>0.5: # calcula el estado de la luz
				state = 'luz encendida'
			else:
				state = 'luz apagada'
			State = np.array([state]) # array a guardar (para usar con np.savetxt)
			np.savetxt('state', State, delimiter=" ", fmt="%s") # garda el txt actualizado
		t1 = time.time() # nuevo tiempo inicial
