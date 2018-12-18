from django.shortcuts import *

def index(request):
	if 'ID' not in request.COOKIES.keys():
		return HttpResponseRedirect(reverse('shop:login'))
	elif request.COOKIES['type'] == 'user':
		return HttpResponseRedirect(reverse('shop:userIndex'))
	else:
		return HttpResponseRedirect(reverse('shop:sellerIndex'))

def userIndex(request, user_id):
	return HttpResponse('You are in user index, id:' + str(user_id))

def sellerIndex(request, seller_id):
	return HttpResponse('You are in seller index, id:' + str(seller_id))
