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

def userIndex(request, user_id):
	rt = {}
	if request.session.get('id', None) == user_id and request.session.get('type') == 'user':
		rt['curUser'] = True
	else: rt['curUser'] = False

	curUser = User.objects.get(user_id=user_id)
	rt['user_id'] = curUser.user_id
	rt['user_name'] = curUser.name
	rt['balance'] = curUser.balance

	rt['coupon'] = Coupon.objects.filter(owner__user_id=user_id)
	rt['buy'] = Buy.objects.filter(user_id__user_id=user_id)
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

def deleteCoupon(request, coupon_id):
	Coupon(coupon_id=coupon_id).delete()
	return HttpResponseRedirect(reverse('shop:index'))

def sellerIndex(request, seller_id):
	curUser = User.objects.get(user_id=seller_id)
	return render(request, 'shop/profile.html', {'name':curUser.name})
