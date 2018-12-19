from django.shortcuts import *
from shop.models import *

def index(request):
	user_id, type_ = request.session.get('id', None), request.session.get('type', None)
	if user_id is None:
		return HttpResponseRedirect(reverse('shop:login'))
	elif type_ == 'user':
		return HttpResponseRedirect(reverse('shop:userIndex', args=(user_id,)))
	elif type_ == 'seller':
		return HttpResponseRedirect(reverse('shop:sellerIndex', args=(user_id,)))

def userIndex(request, user_id):
	rt = {}
	if request.session.get('id', None) == user_id and request.session.get('type') == 'user':
		rt['curUser'] = True
	else: rt['curUser'] = False

	curUser = User.objects.get(user_id=user_id)
	rt['user_id'] = curUser.user_id
	rt['user_name'] = curUser.name
	rt['balance'] = curUser.balance

	rt['coupon'] = Own_coupon.objects.filter(user_id__user_id=user_id)
	rt['buy'] = Buy.objects.filter(user_id__user_id=user_id)
	rt['mark'] = mark.objects.filter(user_id__user_id=user_id)
	rt['trolley'] = shopping_cart.objects.filter(user_id__user_id=user_id)

	return render(request, 'shop/userProfile.html', rt)

def sellerIndex(request, seller_id):
	curUser = User.objects.get(user_id=seller_id)
	return render(request, 'shop/profile.html', {'name':curUser.name})
