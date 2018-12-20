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

    if request.POST['sort'] != '':
      sortKey = request.POST['sortType'] + request.POST['sort']
      computer = computer.order_by(sortKey)

  ctx['computer'] = computer
  return render(request, "shop/computers.html", ctx)

def details(request, computer_id):
  rtx = {}
  rtx['computer'] = get_object_or_404(Computer, pk=computer_id)
  rtx['markAmount'] = mark.objects.filter(computer_id__computer_id=computer_id).count()
  rtx['sell'] = Sell.objects.filter(computer_id__computer_id=computer_id)
  rtx['user_id'] = request.session['id']
  rtx['sellAmount'] = Buy.objects.filter(computer_id__computer_id=computer_id).count()
  rtx['comments'] = computer_comment.objects.filter(computer_id__computer_id=computer_id)
  return render(request, 'shop/computerDetail.html', rtx)

def post(request, user_id, computer_id):
  if request.method == 'POST':
    computer = Computer.objects.get(pk=computer_id)
    user = User.objects.get(pk=user_id)
    computer_comment(computer_id=computer, user_id=user, content=request.POST['comment']).save()
  
  return HttpResponseRedirect(reverse('shop:computerDetail', args=(computer_id, )))