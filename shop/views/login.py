from django.http import HttpResponse, Http404
from django.shortcuts import *
from shop.models import *
from django.db import transaction

import hashlib

def md5Encode(s):
  m = hashlib.md5()
  m.update(s.encode(encoding='utf-8'))
  return m.hexdigest()

@transaction.atomic
def login(request):
	rt = {'error_message': ''}
	if request.method == 'GET':
		return render(request, 'Dashio/login.html', rt)
		
	elif request.method == 'POST':
		if request.POST['type'] == 'user':
			try:
				user_id = int(request.POST['user_id'])
				psw = request.POST['psw']
			except ValueError:
				rt['error_message'] = '账号不存在'
				return render(request, 'Dashio/login.html', rt)

			q = User.objects.filter(user_id=user_id)
			if not q.exists():
				rt['error_message'] = '账号不存在'
				return render(request, 'Dashio/login.html', rt)
			
			if md5Encode(str(psw)) != q[0].password:
				rt['error_message'] = '密码错误'
				return render(request, 'Dashio/login.html', rt)
			
			request.session['id'], request.session['type'] = user_id, 'user'
			return HttpResponseRedirect(reverse('shop:userIndex', args=(user_id, )))

		elif request.POST['type'] == 'seller':
			try:
				seller_id = int(request.POST['user_id'])
				psw = request.POST['psw']
			except ValueError:
				rt['error_message'] = '账号不存在'
				return render(request, 'Dashio/login.html', rt)

			q = Seller.objects.filter(seller_id=seller_id)
			if not q.exists():
				rt['error_message'] = '账号不存在'
				return render(request, 'Dashio/login.html', rt)
			
			if md5Encode(str(psw)) != q[0].password:
				rt['error_message'] = '密码错误'
				return render(request, 'Dashio/login.html', rt)

			request.session['id'], request.session['type'] = seller_id, 'seller'
			return HttpResponseRedirect(reverse('shop:sellerIndex', args=(seller_id, )))

@transaction.atomic
def register(request):
	rt = {'error_message': ''}
	if request.method == 'GET':
		return render(request, 'Dashio/register.html', rt)
	elif request.method == 'POST':
		user_name = request.POST['user_name']
		psw = request.POST['psw']
		psw_confirm = request.POST['psw_confirm']
		address = request.POST['address']
		sex = request.POST['sex']
		type_ = request.POST['type']

		if not user_name: rt['error_message'] = '用户名不能为空'
		if not psw: rt['error_message'] = '密码不能为空'
		if not address: rt['error_message'] = '地址不能为空'
		if psw != psw_confirm: rt['error_message'] = '两次输入密码不一致'

		if rt['error_message']:
			return render(request, 'Dashio/register.html', rt)
		
		if type_ == 'user':
			new_user = User(name=user_name, password=md5Encode(str(psw)), sex=sex, address=address)
			new_user.save()
			request.session['id'], request.session['type'] = new_user.user_id, 'user'
			return HttpResponseRedirect(reverse('shop:userIndex', args=(new_user.user_id,)))
		elif type_ == 'seller':
			new_seller = Seller(name=user_name, password=md5Encode(str(psw)))
			new_seller.save()
			request.session['id'], request.session['type'] = new_seller.seller_id, 'seller'
			return HttpResponseRedirect(reverse('shop:sellerIndex', args=(new_seller.seller_id, )))

def logout(request):
	request.session['id'], request.session['type'] = None, None
	return HttpResponseRedirect(reverse('shop:login'))