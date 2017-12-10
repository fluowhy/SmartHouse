# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
import numpy as np



def hello(request):
	a = np.genfromtxt('/home/mauricio/Documents/Smart/state', dtype='str')
	print a
	text = '<h1>'+'Light '+a[0]+' '+a[2] + '</h1>'+'</br>'+'Última actualización: '+a[3]+' '+a[4]+' '+a[5]+' '+a[6]+' '
	print text
	return HttpResponse(text)
