from django.shortcuts import *

def index(request):
	user_id, type_ = request.session.get('id', None), request.session.get('type', None)
	if user_id is None:
		return HttpResponseRedirect(reverse('shop:login'))
	elif type_ == 'user':
		return HttpResponseRedirect(reverse('shop:userIndex', args=(user_id,)))
	elif type_ == 'seller':
		return HttpResponseRedirect(reverse('shop:sellerIndex', args=(user_id,)))

def userIndex(request, user_id):
	return HttpResponse('You are in user index, id:' + str(user_id))

def sellerIndex(request, seller_id):
	return HttpResponse('You are in seller index, id:' + str(seller_id))
