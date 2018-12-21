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
	rtx['sellAmount'] = Buy.objects.filter(shop_id=rtx['shop'], buy_time__gte=now().date() - timedelta(30)).aggregate(Sum('price'))[r'price__sum']
	if rtx['sellAmount'] is None: rtx['sellAmount'] = 0.0
	rtx['buys'] = Buy.objects.filter(shop_id=rtx['shop']).order_by('buy_time')[:5]
	rtx['comments'] = Shop_comment.objects.filter(shop_id=rtx['shop']).order_by('-comment_date')

	sell = Sell.objects.filter(shop_id=rtx['shop'])
	rtx['sell'] = []
	for s in sell:
		rtx['sell'].append((s.id, s.computer_id.computer_id, s.computer_id.cpu, s.computer_id.memory, s.computer_id.brand.name, s.onsell_date, s.price, Buy.objects.filter(shop_id=s.shop_id, computer_id=s.computer_id).count()))

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

@transaction.atomic
def post(request, user_id, shop_id):
  if request.method == 'POST':
    shop = Shop.objects.get(pk=shop_id)
    user = User.objects.get(pk=user_id)
    Shop_comment(shop_id=shop, user_id=user, content=request.POST['comment']).save()
  
  return HttpResponseRedirect(reverse('shop:shopDetail', args=(shop_id, )))

@transaction.atomic
def manage(request, shop_id):
	shop = get_object_or_404(Shop, pk=shop_id)
	if request.session['type'] != 'seller' or request.session['id'] != shop.seller.seller_id:
		return render(request, 'shop/error.html', {'error': '您不能管理不属于自己的店铺'})
	
	rtx = {}
	rtx['shop'] = shop

	sell = Sell.objects.filter(shop_id=shop)
	rtx['sell'] = []
	for s in sell:
		rtx['sell'].append((s.computer_id.computer_id, s.computer_id.brand.name, s.onsell_date, s.price, Buy.objects.filter(computer_id=s.computer_id, shop_id=s.shop_id).count()))

	rtx['unsell'] = []
	computers = Computer.objects.all()
	for c in computers:
		if c.sell_set.filter(shop_id=shop).count() == 0:
			rtx['unsell'].append((c.computer_id, c.brand.name))

	return render(request, 'shop/shopManage.html', rtx)


@transaction.atomic
def computerManage(request, shop_id, computer_id):
	sell = get_object_or_404(Sell, shop_id__shop_id=shop_id, computer_id__computer_id=computer_id)
	if request.method == 'POST' and request.POST['newPrice'] != '':
		sell.price = float(request.POST['newPrice'])
		sell.save()
	
	rtx = {'computer': sell.computer_id, "shop_id": shop_id, "price": sell.price}

	return render(request, 'shop/shopComputerManage.html', rtx)

@transaction.atomic
def computerAdd(request, shop_id, computer_id):
	computer = get_object_or_404(Computer, pk=computer_id)
	rtx = {'computer': computer, 'shop_id': shop_id, 'error': ''}

	if request.method == 'GET':
		return render(request, 'shop/shopComputerAdd.html', rtx)
	
	elif request.method == 'POST':
		if request.POST['newPrice'] == '':
			rtx['error'] = '请设置价格!'
			return render(request, 'shop/shopComputerAdd.html', rtx)
		else:
			Sell(computer_id=computer, shop_id=get_object_or_404(Shop, pk=shop_id), price=float(request.POST['newPrice'])).save()
			return HttpResponseRedirect(reverse('shop:shopManage', args=(shop_id, )))

@transaction.atomic
def computerDelete(request, shop_id, computer_id):
	sell = get_object_or_404(Sell, shop_id__shop_id=shop_id, computer_id__computer_id=computer_id)
	sell.delete()
	return HttpResponseRedirect(reverse('shop:shopManage', args=(shop_id, )))
