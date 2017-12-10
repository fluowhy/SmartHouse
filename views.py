# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
import numpy as np



def hello(request):
	a = np.genfromtxt('/home/mauricio/Documents/Smart/state', dtype='str')
	text = ''
	n = a.shape
	k = 1
	for i in a:
		if k==1:
			text += '<h1>'+'Light '+i[0]+' '+i[2]+'</br>'
		elif k!=n[0] and k!=1:
			text += 'Light '+i[0]+' '+i[2]+'</br>'
		elif k==n[0]:
			text += 'Light '+i[0]+' '+i[2]+'</h1>'
		k += 1		
	#text = """<h1>Hola Mamá soy LucreciaApp !</br></h1>"""
	return HttpResponse(text)
