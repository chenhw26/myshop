from django.shortcuts import *
from shop.models import *
from django.db import transaction
from django.core.exceptions import *

@transaction.atomic
def computers(request):
  ctx = {}
  computer = Computer.objects.all()
  ctx['brand'] = Brand.objects.all()

  if request.method == 'POST':
    if request.POST['computer_id'] != '':
      computer = computer.filter(computer_id__icontains=request.POST['computer_id'])
    if request.POST['cpu'] != '':
      computer = computer.filter(cpu__icontains=request.POST['cpu'])
    if request.POST['graphics_card'] != '':
      computer = computer.filter(graphics_card__icontains=request.POST['graphics_card'])
    
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
      return render(request, 'Dashio/error.html', {'error': "请输入整数"})
    
    if request.POST.get('brand', '') != '':
      print(request.POST['brand'])
      computer = computer.filter(brand__name__icontains=request.POST['brand'])

    if request.POST['sort'] != '':
      sortKey = request.POST['sortType'] + request.POST['sort']
      computer = computer.order_by(sortKey)

  ctx['computer'] = computer
  return render(request, "Dashio/computers.html", ctx)

@transaction.atomic
def details(request, computer_id):
  rtx = {}
  rtx['isUser'] = request.session['type'] == 'user'
  rtx['computer'] = get_object_or_404(Computer, pk=computer_id)
  rtx['markAmount'] = mark.objects.filter(computer_id__computer_id=computer_id).count()
  rtx['sell'] = Sell.objects.filter(computer_id__computer_id=computer_id)
  rtx['user_id'] = request.session['id']
  rtx['sellAmount'] = Buy.objects.filter(computer_id__computer_id=computer_id).count()
  rtx['comments'] = computer_comment.objects.filter(computer_id__computer_id=computer_id).order_by('-comment_date')
  rtx['buys'] = Buy.objects.filter(computer_id__computer_id=computer_id).order_by('-buy_time')[:5]
  
  if rtx['isUser']:
    rtx['mark'] = ('收藏' if mark.objects.filter(user_id__user_id=rtx['user_id'], computer_id=rtx['computer']).count() == 0 else '取消收藏')

  return render(request, 'Dashio/computer_detail.html', rtx)

@transaction.atomic
def post(request, user_id, computer_id):
  if request.method == 'POST':
    computer = Computer.objects.get(pk=computer_id)
    user = User.objects.get(pk=user_id)
    computer_comment(computer_id=computer, user_id=user, content=request.POST['comment']).save()
  
  return HttpResponseRedirect(reverse('shop:computerDetail', args=(computer_id, )))

def makeMark(request, computer_id, user_id):
  try:
    m = mark.objects.get(computer_id__computer_id=computer_id, user_id__user_id=user_id)
    m.delete()
  except ObjectDoesNotExist:
    computer = get_object_or_404(Computer, pk=computer_id)
    user = get_object_or_404(User, pk=user_id)
    mark(computer_id=computer, user_id=user).save()
  
  return HttpResponseRedirect(reverse('shop:computerDetail', args=(computer_id, )))