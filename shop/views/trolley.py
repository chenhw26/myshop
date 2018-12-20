from django.shortcuts import *
from shop.models import *
from django.db import transaction
import datetime

def trolley(request, user_id):
	if not (request.session.get('id', None) == user_id and request.session.get('type', None) == 'user'):
		return HttpResponse("Sorry, 你不能操作他人的购物车")
	
	trolley = shopping_cart.objects.filter(user_id__user_id=user_id)
	if not trolley.exists():
		return render(request, "shop/notice.html", {'notice': "你的购物车空空如也"})
		
	coupon = Coupon.objects.filter(owner__user_id=user_id, expired__gte=datetime.datetime.now())

	# rt['trolley'][i][0] = computer_id, rt['trolley'][i][1] = shop_id, rt['trolley'][i][2] = shop_name, rt['trolley'][i][3] = price, rt['trolley'][i][4] = shopping_cart.id
	rt = {'trolley': trolley, 'coupon': coupon, 'name': User.objects.get(user_id=user_id).name, 'total': 0.0, 'couponTotal': 0.0, 'user_id': user_id}

	for t in trolley:
		rt['total'] += t.sell.price
	for c in coupon:
		rt['couponTotal'] += c.value
	rt['total'] -= rt['couponTotal']
	if rt['total'] < 0: rt['total'] = 0.0
	
	return render(request, 'shop/trolley.html', rt)

@transaction.atomic
def buy(request, user_id):
	# 清空购物车，清空优惠券，添加订单，改变余额
	trolley = shopping_cart.objects.filter(user_id__user_id=user_id)
	curUser = User.objects.get(user_id=user_id)
	coupon = Coupon.objects.filter(owner__user_id=user_id, expired__gte=datetime.datetime.now())
	
	total, couponTotal = 0.0, 0.0
	for t in trolley:
		total += t.sell.price
	for c in coupon:
		couponTotal += c.value
	total -= couponTotal
	if total < 0: total = 0.0

	if total > curUser.balance:
		return render(request, 'shop/error.html', {'error': '您的余额不足'})
	
	for c in trolley:
		Buy(computer_id=c.sell.computer_id, shop_id=c.sell.shop_id, user_id=c.user_id, price=c.sell.price).save()
		seller = Seller.objects.get(seller_id=c.sell.shop_id.seller.seller_id)
		seller.balance += c.sell.price
		seller.save()

	trolley.delete()
	coupon.delete()
	curUser.balance -= total
	curUser.save()
	return render(request, 'shop/notice.html', {'notice': '购买成功，谢谢惠顾!'})

@transaction.atomic
def add(request, sell_id, user_id):
	curUser = User.objects.get(user_id=user_id)
	sell = get_object_or_404(Sell, pk=sell_id)
	shopping_cart(sell=sell, user_id=curUser).save()
	return render(request, 'shop/addTrolley.html', {'user_id': user_id, 'computer_id': sell.computer_id.computer_id})

@transaction.atomic
def delete(request, trolley_id):
	trolley = shopping_cart.objects.get(id=trolley_id)
	user_id = trolley.user_id.user_id
	trolley.delete()
	return HttpResponseRedirect(reverse('shop:trolley', args=(user_id, )))