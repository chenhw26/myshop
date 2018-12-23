from django.shortcuts import *
from shop.models import *
from django.db import transaction
from django.utils.timezone import now, timedelta
from django.db.models import Sum
from django.db import connection

@transaction.atomic
def sellerIndex(request, seller_id):
	rtx = {}
	if not (request.session['id'] == seller_id and request.session['type'] == 'seller'):
		rtx['curSeller'] = False
	else: rtx['curSeller'] = True

	curSeller = Seller.objects.get(seller_id=seller_id)
	rtx['seller'] = curSeller
	rtx['user_type'] = '卖家'
	rtx['sells'] = Buy.objects.filter(shop_id__seller=curSeller).order_by('-buy_time')[:5]
	rtx['turnover'] = Buy.objects.filter(shop_id__seller=curSeller, buy_time__gte=now().date()-timedelta(30)).aggregate(Sum('price'))[r'price__sum']
	if rtx['turnover'] is None:
		rtx['turnover'] = 0.0

	with connection.cursor() as cursor:
		cursor.execute('''select shop_id, name, city, open_date, SUM(price) as turnover
                      from shop_shop left join shop_buy on shop_id=shop_id_id
                      where shop_shop.seller_id=%s
                      group by shop_id, name, city, open_date''', [seller_id])
		rtx['shops'] = cursor.fetchall()
	
	return render(request, 'Dashio/seller.html', rtx)

@transaction.atomic
def openShop(request, seller_id):
	if not(request.session.get('id', '') == seller_id and request.session.get('type', '') == 'seller'):
		return render(request, 'Dashio/error.html', {'error': '账号错误'})
	
	if request.method == 'GET':
		return render(request, 'Dashio/openShop.html', {'seller_id': seller_id})
	
	elif request.method == 'POST':
		name, city, address = request.POST['name'], request.POST['city'], request.POST['address']
		if name == '':
			return render(request, 'Dashio/error.html', {'error': '请输入店铺名'})
		if address == '':
			return render(request, 'Dashio/error.html', {'error': '请输入详细地址'})
		try:
			Shop(name=name, city=city, address = address, seller=Seller.objects.get(pk=seller_id)).save()
		except BaseException as e:
			return render(request, 'Dashio/error.html', {'error': e.message})
		
		return render(request, 'Dashio/notice.html', {'notice': '开店成功'})


@transaction.atomic
def sellRecord(request, seller_id):
	rtx = {}
	rtx['seller'] = get_object_or_404(Seller, pk=seller_id)
	rtx['brand'] = Brand.objects.all()
	records = Buy.objects.filter(shop_id__seller=rtx['seller']).order_by('-buy_time')
	
	if request.method == 'POST':
		user = request.POST['user']
		computer_id = request.POST['computer_id']
		brand = request.POST['brand']
		shop = request.POST['shop']
		minDate = request.POST['minDate']
		maxDate = request.POST['maxDate']
		minPrice = request.POST['minPrice']
		maxPrice = request.POST['maxPrice']
		
		if user != '':
			records = records.filter(user_id__name=user)
		if computer_id != '':
			records = records.filter(computer_id__computer_id=computer_id)
		if brand != '':
			records = records.filter(computer_id__brand__name=brand)
		if shop != '':
			records = records.filter(shop_id__name=shop)
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

	return render(request, 'Dashio/sellerRecord.html', rtx)