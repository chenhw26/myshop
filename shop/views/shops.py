from django.shortcuts import *
from shop.models import *
from django.db.models import Sum
from django.utils.timezone import now, timedelta
from django.db import transaction

@transaction.atomic
def shops(request):
	rtx = {'shops': []}
	shops = Shop.objects.all()
	
	if request.method == 'POST':
		name, city, minDate, maxDate, seller = request.POST['name'], request.POST['city'], request.POST['minDate'], request.POST['maxDate'], request.POST['seller']
		if name != '':
			shops = shops.filter(name=name)
		if city != '':
			shops = shops.filter(city=city)
		if seller != '':
			shops = shops.filter(seller__name=seller)
		if minDate != '':
			y, m, d = minDate.split('-')
			shops = shops.filter(open_date__gte=datetime.date(int(y), int(m), int(d)))
		if maxDate != '':
			y, m, d = maxDate.split('-')
			shops = shops.filter(open_date__lte=datetime.date(int(y), int(m), int(d)))

		if request.POST['sort'] not in ('', 'turnover'):
			sortKey = request.POST['sortType'] + request.POST['sort']
			shops = shops.order_by(sortKey)

	for shop in shops:
		turnover = Buy.objects.filter(shop_id__shop_id=shop.shop_id).aggregate(Sum('price'))[r'price__sum']
		if turnover is None: turnover = 0.0
		rtx['shops'].append((shop.shop_id, shop.name, shop.city, shop.open_date, shop.seller.seller_id, shop.seller.name, turnover))
	
	if request.method == 'POST' and request.POST['sort'] == 'turnover':
		rtx['shops'].sort(key=lambda t: t[6], reverse=(request.POST['sortType'] == '-'))
	
	return render(request, 'shop/shops.html', rtx)

@transaction.atomic
def details(request, shop_id):
	rtx = {}
	rtx['isUser'] = (request.session['type'] == 'user')
	rtx['user_id'] = int(request.session['id'])
	
	rtx['shop'] = get_object_or_404(Shop, pk=shop_id)
	rtx['sell'] = Sell.objects.filter(shop_id=rtx['shop'])
	rtx['sellAmount'] = Buy.objects.filter(shop_id=rtx['shop'], buy_time__gte=now().date() - timedelta(30)).aggregate(Sum('price'))[r'price__sum']
	rtx['buys'] = Buy.objects.filter(shop_id=rtx['shop']).order_by('buy_time')[:5]

	rtx['curSeller'] = (not rtx['isUser'] and request.session['id'] == rtx['shop'].seller.seller_id)

	return render(request, 'shop/shopDetail.html', rtx)

@transaction.atomic
def sellRecord(request, shop_id):
	rtx = {}
	rtx['shop'] = get_object_or_404(Shop, pk=shop_id)
	rtx['brand'] = Brand.objects.all()
	records = Buy.objects.filter(shop_id__shop_id=shop_id).order_by('-buy_time')

	if request.method == 'POST':
		computer_id = request.POST['computer_id']
		brand = request.POST['brand']
		user = request.POST['user']
		minDate = request.POST['minDate']
		maxDate = request.POST['maxDate']
		minPrice = request.POST['minPrice']
		maxPrice = request.POST['maxPrice']
		
		if computer_id != '':
			records = records.filter(computer_id__computer_id=computer_id)
		if brand != '':
			records = records.filter(computer_id__brand__name=brand)
		if user != '':
			records = records.filter(user_id__name=user)
		if minDate != '':
			y, m, d = minDate.split('-')
			records = records.filter(buy_time__gte=datetime.date(int(y), int(m), int(d)))
		if maxDate != '':
			y, m, d = maxDate.split('-')
			records = records.filter(buy_time__lte=datetime.date(int(y), int(m), int(d)))
		if minPrice != '':
			records = records.filter(price__gte=float(minPrice))
		if maxPrice != '':
			records = records.filter(price__lte=float(maxPrice))

		if request.POST['sort'] != '':
			sortKey = request.POST['sortType'] + request.POST['sort']
			records = records.order_by(sortKey)

	rtx['records'] = records

	return render(request, 'shop/shopSellRecord.html', rtx)
