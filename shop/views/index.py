from django.shortcuts import HttpResponseRedirect, reverse

def index(request):
	if 'ID' not in request.COOKIES.keys():
		return HttpResponseRedirect(reverse('shop:login'))
	elif request.COOKIES['type'] == 'user':
		return HttpResponseRedirect(reverse('shop:userIndex'))
	else:
		return HttpResponseRedirect(reverse('shop:sellerIndex'))

def userIndex(request, user_id):
	pass

def sellerIndex(request, seller_id):
	pass
