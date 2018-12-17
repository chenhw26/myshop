from django.http import HttpResponse, Http404
from django.shortcuts import *

def login(request):
	if request.method == 'GET':
		return render(request, 'shop/login.html', {})
	if request.method == 'POST':
		return render(request, 'shop/login.html', dict(request.POST))

def register(request):
	pass