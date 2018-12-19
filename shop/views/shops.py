from django.shortcuts import *

def shops(request):
	pass

def details(request, shop_id):
	return HttpResponse(str(shop_id) + ' shop Detail')