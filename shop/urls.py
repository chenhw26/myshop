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
    path('buy/trolley/<int:user_id>/', trolley.buy, name='trolley_buy'),
    path('add/trolley/<str:sell_id>/<int:user_id>/', trolley.add, name='trolley_add'),
    path('delete/trolley/<int:trolley_id>/', trolley.delete, name='trolley_delete'),
    path('brand/detail/<str:name>/', brand.brand, name='brand'),
    path('recharge/<int:user_id>', user.recharge, name='recharge'),
    path('coupon/get/<int:user_id>/', user.getCoupon, name='getCoupon'),
    path('coupon/delete/<int:coupon_id>/', user.deleteCoupon, name='deleteCoupon'),
    path('buy/record/<int:user_id>/', user.buyRecord, name='buyRecord'),
    path('computers/details/post/<int:user_id>/<str:computer_id>/', computers.post, name='postComputerComment'),
    path('seller/openshop/<int:seller_id>/', seller.openShop, name='openShop'),
    path('seller/record/<int:seller_id>/', seller.sellRecord, name='sellerRecord'),
    path('shop/record/<int:shop_id>/', shops.sellRecord, name='shopSellRecord'),
    path('shop/details/post/<int:user_id>/<int:shop_id>/', shops.post, name='postShopComment'),
    path('shop/manage/<int:shop_id>/', shops.manage, name='shopManage'),
    path('shop/manage/computer/<int:shop_id>/<str:computer_id>/', shops.computerManage, name='shopComputerManage'),
    path('shop/add/<int:shop_id>/computer/<str:computer_id>/', shops.computerAdd, name='shopComputerAdd'),
    path('shop/delete/<int:shop_id>/computer/<str:computer_id>/', shops.computerDelete, name='shopComputerDelete'),
    path('computers/detail/<str:computer_id>/mark/<int:user_id>/', computers.makeMark, name='mark'),
    path('brand/like/<str:name>/<int:user_id>/', brand.makeLike, name='like'),
    path('all/brand/', brand.allBrands, name='allBrands'),
]