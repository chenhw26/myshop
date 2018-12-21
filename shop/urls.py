from django.urls import path
from .views import user, seller, login, shops, computers, trolley, brand

app_name = 'shop'  #声明namespace

urlpatterns = [
    path('', user.index, name='index'),
    path('login/', login.login, name='login'),
    path('register/', login.register, name='register'),
    path('logout/', login.logout, name='logout'),
    path('user/index/<int:user_id>/', user.userIndex, name='userIndex'),
    path('seller/index/<int:seller_id>/', seller.sellerIndex, name='sellerIndex'),
    path('shops/', shops.shops, name='shops'),
    path('computers/', computers.computers, name='computers'),
    path('computers/details/<str:computer_id>/', computers.details, name='computerDetail'),
    path('shops/details/<int:shop_id>/', shops.details, name='shopDetail'),
    path('trolley/<int:user_id>/', trolley.trolley, name='trolley'),
    path('trolley/<int:user_id>/buy/', trolley.buy, name='trolley_buy'),
    path('trolley/add/<str:sell_id>/<int:user_id>/', trolley.add, name='trolley_add'),
    path('trolley/delete/<int:trolley_id>/', trolley.delete, name='trolley_delete'),
    path('brand/<str:name>/', brand.brand, name='brand'),
    path('recharge/<int:user_id>', user.recharge, name='recharge'),
    path('coupon/get/<int:user_id>/', user.getCoupon, name='getCoupon'),
    path('coupon/delete/<int:coupon_id>/', user.deleteCoupon, name='deleteCoupon'),
    path('buy/record/<int:user_id>/', user.buyRecord, name='buyRecord'),
    path('computers/details/post/<int:user_id>/<str:computer_id>/', computers.post, name='postComputerComment'),
    path('seller/openshop/<int:seller_id>/', seller.openShop, name='openShop'),
    path('seller/record/<int:seller_id>/', seller.sellRecord, name='sellerRecord'),
    path('shop/record/<int:shop_id>/', shops.sellRecord, name='shopSellRecord'),
]

# urlpatterns = [
#     path('', views.IndexView.as_view(), name='index'),
#     path('<int:pk>/', views.DetailView.as_view(), name='detail'),
#     path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
#     path('<int:question_id>/vote/', views.vote, name='vote'),
# ]