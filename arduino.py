# -*- coding: utf-8 -*-

from __future__ import division
import numpy as np
import time
import pyfirmata
import datetime

# Este programa lee los pines analogico 0 y digital 2 de un arduino uno a traves
# del puerto USB y guarda un archivo de texto con la informacion del estado de 
# una luz ficticia representada por un LDR. Ademas muestra el voltaje digital
# promedio y analogico respectivos.

def estado(value):
	# determina el estado de una luz
	if value>0.5: # calcula el estado de la luz
		state = 'luz ON'
	else:
		state = 'luz OFF'
	return state		

port = '/dev/ttyACM1' # puerto donde esta conectado el arduino (hay que cambiarlo dependiendo del pc)
board = pyfirmata.Arduino(port) # crea objeto como arduino en puerto anterior

it = pyfirmata.util.Iterator(board) # para que el buffer no haga overflow
it.start()

A0 = board.get_pin('a:0:i') # define pin analogico A0 como input
D2 = board.get_pin('d:2:o') # define pin digital D2 como input (ampolleta 1)
dt1 = 1 # tiempo de actualizacion en segundos
t1 = time.time() # toma tiempo inicial
state = 0
while True:
	t2 = time.time() # toma tiempo final
	dt = t2 - t1 # calcula dt
	if dt >= dt1: # si dt > 10 segundos calcula estado de las luces
		k = 0 # muestras reales (hay problema con muestras None)
		lec = 0 # guarda estado pin analogico (prueba)
		for i in range(10): # el estado de las luces se calcula con un promedio de 10 muestras
			a = A0.read() # lee pin analogico 0 
			if a!=None: # condicion para que no hayan NoneType
				k += 1
				lec += a
		lec = lec/k
		print lec
		Th = int(datetime.datetime.now().strftime('%H'))
		Tm = int(datetime.datetime.now().strftime('%M'))
		if lec<0.1: # lec<0.1 hay persona	 
			if Th>=13 or Th<=7:
				state = 1		
			else:
				state = 0
		else:
			state = 0
		if k!=0:		
			State = np.array([[1, estado(state)]]) # array a guardar (para usar con np.savetxt)
			np.savetxt('state', State, delimiter=" ", fmt="%s") # garda el txt actualizado	
		D2.write(state)
		t1 = time.time() # nuevo tiempo inicial
