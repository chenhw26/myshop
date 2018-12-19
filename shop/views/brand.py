from shop.models import *
from django.shortcuts import *

def brand(request, name):
	return render(request, 'shop/brand.html', {'name': name})