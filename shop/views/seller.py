from django.shortcuts import *
from shop.models import *
from django.db import transaction
from django.utils.timezone import now, timedelta

def sellerIndex(request, seller_id):
	curUser = User.objects.get(user_id=seller_id)
	return render(request, 'shop/profile.html', {'name':curUser.name})
