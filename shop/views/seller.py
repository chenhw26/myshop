from django.shortcuts import *
from shop.models import *
from django.db import transaction
from django.utils.timezone import now, timedelta
from django.db.models import Sum

def sellerIndex(request, seller_id):
	rtx = {}
	if not (request.session['id'] == seller_id and request.session['type'] == 'seller'):
		rtx['curSeller'] = False
	else: rtx['curSeller'] = True

	curSeller = Seller.objects.get(seller_id=seller_id)
	rtx['seller'] = curSeller
	rtx['turnover'] = Buy.objects.filter(shop_id__seller=curSeller, buy_time__gte=now().date()-timedelta(30)).aggregate(Sum('price'))
	rtx['shops'] = Shop.objects.filter(seller=curSeller)

	return render(request, 'shop/sellerProfile.html', rtx)

def openShop(request, seller_id):
	return HttpResponse('kaidian')