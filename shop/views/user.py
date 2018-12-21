from django.shortcuts import *
from shop.models import *
from django.db import transaction
from django.utils.timezone import now, timedelta

def index(request):
	user_id, type_ = request.session.get('id', None), request.session.get('type', None)
	if user_id is None:
		return HttpResponseRedirect(reverse('shop:login'))
	elif type_ == 'user':
		return HttpResponseRedirect(reverse('shop:userIndex', args=(user_id,)))
	elif type_ == 'seller':
		return HttpResponseRedirect(reverse('shop:sellerIndex', args=(user_id,)))

@transaction.atomic
def userIndex(request, user_id):
	rt = {}
	if request.session.get('id', None) == user_id and request.session.get('type') == 'user':
		rt['curUser'] = True
	else: rt['curUser'] = False

	curUser = get_object_or_404(User, user_id=user_id)
	rt['user_id'] = curUser.user_id
	rt['user_name'] = curUser.name
	rt['balance'] = curUser.balance

	rt['coupon'] = Coupon.objects.filter(owner__user_id=user_id)
	rt['buy'] = Buy.objects.filter(user_id__user_id=user_id).order_by('-buy_time')[:5]
	rt['mark'] = mark.objects.filter(user_id__user_id=user_id)
	rt['trolley'] = shopping_cart.objects.filter(user_id__user_id=user_id)

	return render(request, 'shop/userProfile.html', rt)

@transaction.atomic
def recharge(request, user_id):
	if not (request.session.get('id', None) == user_id and request.session.get('type', None) == 'user'):
		return render(request, 'shop/error.html', {'error': '你不能为他人充值'})
	
	if request.method == 'GET':
		return render(request, 'shop/recharge.html', {'user_id': user_id})
	elif request.method == 'POST':
		if request.POST['value'] == '':
			return render(request, 'shop/error.html', {'error': '请输入一个数值'})
		
		value = int(request.POST['value'])
		curUser = User.objects.get(user_id=user_id)
		curUser.balance += value
		curUser.save()

		return render(request, 'shop/notice.html', {'notice': '您已成功充值'+str(value)+'元'})

@transaction.atomic
def getCoupon(request, user_id):
	if not (request.session.get('id', None) == user_id and request.session.get('type', None) == 'user'):
		return render(request, 'shop/error.html', {'error': '你不能为他人领取代金券'})
	
	if request.method == 'GET':
		return render(request, 'shop/getCoupon.html', {'user_id': user_id})
	elif request.method == 'POST':
		if request.POST.get('value', '') == '':
			if request.POST['userDefinedValue'] == '':
				return render(request, 'shop/error.html', {'error': '请输入一个数值'})
			else: value = int(request.POST['userDefinedValue'])
		else: value = int(request.POST['value'])

		curUser = User.objects.get(user_id=user_id)
		Coupon(value=value, owner=curUser, expired= now().date()+timedelta(days=7)).save()

		return render(request, 'shop/notice.html', {'notice': '您已成功领取'+str(value)+'元代金券'})

@transaction.atomic
def deleteCoupon(request, coupon_id):
	Coupon(coupon_id=coupon_id).delete()
	return HttpResponseRedirect(reverse('shop:index'))

@transaction.atomic
def buyRecord(request, user_id):
	rtx = {}
	rtx['user'] = get_object_or_404(User, pk=user_id)
	rtx['brand'] = Brand.objects.all()
	records = Buy.objects.filter(user_id__user_id=user_id)

	if request.method == 'POST':
		computer_id = request.POST['computer_id']
		brand = request.POST['brand']
		shop = request.POST['shop']
		minDate = request.POST['minDate']
		maxDate = request.POST['maxDate']
		minPrice = request.POST['minPrice']
		maxPrice = request.POST['maxPrice']
		
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

	rtx['records'] = records.order_by('-buy_time')

	return render(request, 'shop/buyRecord.html', rtx)