from django.shortcuts import *
from shop.models import *

def computers(request):
  ctx = {}
  computer = Computer.objects.all()
  ctx['brand'] = Brand.objects.all()

  if request.method == 'POST':
    if request.POST['computer_id'] != '':
      computer = computer.filter(computer_id=request.POST['computer_id'])
    if request.POST['cpu'] != '':
      computer = computer.filter(cpu=request.POST['cpu'])
    if request.POST['graphics_card'] != '':
      computer = computer.filter(graphics_card=request.POST['graphics_card'])
    
    try:
      if request.POST['minMemory'] != '':
        computer = computer.filter(memory__gte=int(request.POST['minMemory']))
      if request.POST['maxMemory'] != '':
        computer = computer.exclude(memory__gte=int(request.POST['maxMemory']))

      if request.POST['minssd'] != '':
        computer = computer.filter(ssd_capacity__gte=int(request.POST['minssd']))
      if request.POST['maxssd'] != '':
        computer = computer.exclude(ssd_capacity__gte=int(request.POST['maxssd']))

      if request.POST['minDisk'] != '':
        computer = computer.filter(disk_capacity__gte=int(request.POST['minDisk']))
      if request.POST['maxDisk'] != '':
        computer = computer.exclude(disk_capacity__gte=int(request.POST['maxDisk']))

    except ValueError:
      return render(request, 'shop:error.html', {'error': "请输入整数"})
    
    if request.POST.get('brand', '') != '':
      print(request.POST['brand'])
      computer = computer.filter(brand__name=request.POST['brand'])

  ctx['computer'] = computer
  return render(request, "shop/computers.html", ctx)

def details(request, computer_id):
	return HttpResponse(str(computer_id) + 'detail')