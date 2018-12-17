from django.urls import path
from .views import index, login, shops, computers, trolley

app_name = 'shop'  #声明namespace

urlpatterns = [
    path('', index.index),
    path('login/', login.login, name='login'),
    path('register/', login.register, name='register'),
    path('userIndex/<int:user_id>/', index.userIndex, name='userIndex'),
    path('sellerIndex/<int:seller_id>/', index.sellerIndex, name='sellerIndex'),
    path('shops/', shops.shops, name='shops'),
    path('computers/', computers.computers, name='computers'),
    path('computers/details/<str:computer_id>/', computers.details, name='computerDetail'),
    path('shops/details/<int:shop_id>/', shops.details, name='shopDetail'),
    path('trolley/<int:user_id>/', trolley.trolley, name='trolley')
]

# urlpatterns = [
#     path('', views.IndexView.as_view(), name='index'),
#     path('<int:pk>/', views.DetailView.as_view(), name='detail'),
#     path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
#     path('<int:question_id>/vote/', views.vote, name='vote'),
# ]