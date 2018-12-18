from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Computer(models.Model):
	# 笔记本型号
	computer_id = models.CharField(max_length=30, primary_key=True)
	# cpu型号
	cpu = models.CharField(max_length=15)
	# 显卡型号
	graphics_card = models.CharField(max_length=15, null=True)
	# 以GB为单位
	memory = models.IntegerField(validators=[MaxValueValidator(128), MinValueValidator(0)])
	ssd_capacity = models.IntegerField(validators=[MinValueValidator(0)], null=True)
	disk_capacity = models.IntegerField(validators=[MinValueValidator(0)], null=True)
	screen_size = models.CharField(max_length=10)

class Shop(models.Model):
	# 店铺id
	shop_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	address = models.CharField(max_length=50)
	open_date = models.DateField(auto_now=False, auto_now_add=False)

class Brand(models.Model):
	name = models.CharField(max_length=15, primary_key=True)
	country = models.CharField(max_length=15)
	found_date = models.DateField(auto_now=False, auto_now_add=False)
	net = models.CharField(max_length=50, null=True)

class Seller(models.Model):
	seller_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	password = models.CharField(max_length=100)
	balance = models.FloatField(validators=[MinValueValidator(0)], default=0)

class User(models.Model):
	user_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	password = models.CharField(max_length=100)
	sex = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female')))
	address = models.CharField(max_length=50)
	balance = models.FloatField(validators=[MinValueValidator(0)], default=100000)

# 优惠券表
class Coupon(models.Model):
	coupon_id = models.AutoField(primary_key=True)
	# 该优惠券可减免的价格
	value = models.FloatField(validators=[MinValueValidator(0)])

# 表示用户拥有优惠券的表
class Own_coupon(models.Model):
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)
	coupon_id = models.ForeignKey(Coupon, on_delete=models.CASCADE)
	class Meta:
		# 表明(user_id, coupon)作为联合主键
		unique_together = ("user_id", "coupon_id")

# 用户对店铺的评论
class Shop_comment(models.Model):
	comment_id = models.AutoField(primary_key=True)
	shop_id = models.ForeignKey(Shop, on_delete=models.CASCADE)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)
	content = models.TextField()

# 表示优惠券的适用店铺的表
class Available(models.Model):
	shop_id = models.ForeignKey(Shop, on_delete=models.CASCADE)
	coupon_id = models.ForeignKey(Coupon, on_delete=models.CASCADE)
	class Meta:
		unique_together = ('shop_id', 'coupon_id')

# 表示店铺销售电脑的表
class Sell(models.Model):
	computer_id = models.ForeignKey(Computer, on_delete=models.CASCADE)
	shop_id = models.ForeignKey(Shop, on_delete=models.CASCADE)
	price = models.FloatField(validators=[MinValueValidator(0)])
	# 上架日期
	onsell_date = models.DateField(auto_now=False, auto_now_add=True)
	class Meta:
		unique_together = ('computer_id', 'shop_id')

# 用户的购买记录
class Buy(models.Model):
	# 允许同一个用户在同一个商店多次购买同一款电脑，所以需要额外的主键
	buy_id = models.AutoField(primary_key=True)
	computer_id = models.ForeignKey(Computer, on_delete=models.CASCADE)
	shop_id = models.ForeignKey(Shop, on_delete=models.CASCADE)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)
	buy_time = models.DateField(auto_now=False, auto_now_add=True)
	price = models.FloatField(validators=[MinValueValidator(0)])

# 表示用户收藏某一型号电脑的表
class mark(models.Model):
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)
	computer_id = models.ForeignKey(Computer, on_delete=models.CASCADE)
	mark_date = models.DateField(auto_now=False, auto_now_add=True)
	class Meta:
		unique_together = ('user_id', 'computer_id')

class computer_comment(models.Model):
	computer_comment_id = models.AutoField(primary_key=True)
	computer_id = models.ForeignKey(Computer, on_delete=models.CASCADE)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)
	comment_date = models.DateField(auto_now=False, auto_now_add=True)
	content = models.TextField()

# 用户为某电脑品牌点赞
class like(models.Model):
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)
	brand_name = models.ForeignKey(Brand, on_delete=models.CASCADE)
	class Meta:
		unique_together = ('user_id', 'brand_name')

# 某个型号的电脑属于某个品牌
class produce(models.Model):
	computer_id = models.ForeignKey(Computer, on_delete=models.CASCADE)
	brand_name = models.ForeignKey(Brand, on_delete=models.CASCADE)
	class Meta:
		unique_together = ('computer_id', 'brand_name')

# 某个店铺属于某个卖家
class belong(models.Model):
	shop_id = models.ForeignKey(Shop, on_delete=models.CASCADE)
	seller_id = models.ForeignKey(Seller, on_delete=models.CASCADE)
	class Meta:
		unique_together = ('shop_id', 'seller_id')

# 购物车
class trolley(models.Model):
	computer_id = models.ForeignKey(Computer, on_delete=models.CASCADE)
	shop_id = models.ForeignKey(Shop, on_delete=models.CASCADE)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)
	class Meta:
		unique_together = ('computer_id', 'shop_id', 'user_id')
