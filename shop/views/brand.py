from shop.models import *
from django.shortcuts import *
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist

def brand(request, name):
	rtx = {}
	rtx['isUser'] = request.session.get('type', '') == 'user'
	rtx['user_id'] = request.session.get('id', '')

	rtx['brand'] = Brand.objects.get(pk=name)
	rtx['turnover'] = Buy.objects.filter(computer_id__brand=rtx['brand']).aggregate(Sum('price'))[r'price__sum']
	rtx['likeNumber'] = like.objects.filter(brand_name=rtx['brand']).count()
	rtx['followers'] = like.objects.filter(brand_name=rtx['brand'])

	rtx['like'] = '取消关注' if like.objects.filter(brand_name__name=name, user_id__user_id=rtx['user_id']).count() > 0 else '关注'

	rtx['computers'] = []
	for c in Computer.objects.filter(brand__name=name):
		rtx['computers'].append((c.computer_id, c.cpu, c.memory, Buy.objects.filter(computer_id__brand__name=name).count()))

	rtx['net'] = rtx['brand'].net
	if rtx['net'][:4] != 'http':
		rtx['net'] = 'http://' + rtx['net']

	return render(request, 'shop/brand.html', rtx)

def makeLike(request, name, user_id):
  try:
    m = like.objects.get(brand_name__name=name, user_id__user_id=user_id)
    m.delete()
  except ObjectDoesNotExist:
    brand = get_object_or_404(Brand, pk=name)
    user = get_object_or_404(User, pk=user_id)
    like(brand_name=brand, user_id=user).save()
  
  return HttpResponseRedirect(reverse('shop:brand', args=(name, )))

def allBrands(request):
	brands = Brand.objects.all()
	rtx = {'brands': []}
	for b in brands:
		rtx['brands'].append((b.name, b.country, b.found_date, Computer.objects.filter(brand=b).count(), Buy.objects.filter(computer_id__brand=b).aggregate(Sum('price'))[r'price__sum']))
	
	if request.method == 'POST':
		sortKey = {'name': 0, 'country': 1, 'found_date': 2, 'computerNumber': 3, 'turnover': 4}
		rtx['brands'].sort(key=lambda x: x[sortKey[request.POST['sort']]], reverse=(request.POST['sortType'] == '-'))
	
	return render(request, 'shop/allBrands.html', rtx)