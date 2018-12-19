from django.shortcuts import *
from shop.models import *

def computers(request):
  ctx = {}
  if request.POST:
    ctx['computers'] = request.POST['computers']
  return render(request, "shop/computers.html", ctx)

def details(request, computer_id):
	return HttpResponse(str(computer_id) + 'detail')