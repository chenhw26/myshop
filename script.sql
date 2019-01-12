use OnlineShop;
begin tran
	insert into shop_brand values('Lenovo', 'China', '1984-10-17', 'www.lenovo.com');
	insert into shop_brand values('Apple', 'USA', '1976-4-1', 'www.apple.com');
	insert into shop_brand values('Dell', 'USA', '1989-11-4', 'www.dell.com');
	insert into shop_brand values('ASUS', 'Taiwan', '1989-4-2', 'www.asus.com');
	insert into shop_brand values('VAIO', 'Japan', '2014-7-1', 'us.vaio.com');
commit tran

begin tran
	insert into shop_computer values('ThinkPad L380', 'i5-8250U', 'Intel® UHD Graphics 620', 32, 512, 1024, '13.3', 'Lenovo');
	insert into shop_computer values('昭阳 K42', 'i5-7200U', 'nVIDIA G940MX', 8, 256, 512, '14.0', 'Lenovo');
	insert into shop_computer values('扬天 V530s', 'i7-8700U', 'Nvidia GeForce MX150', 8, 128, null, '14.0', 'Lenovo');
	insert into shop_computer values('ThinkPad A485', 'Ryzen™ 7 PRO 2700U', 'Radeon® Vega Graphics', 32, 128, 500, '14.0', 'Lenovo');
	insert into shop_computer values('ThinkPad X1 Yoga 2018', 'i5-8250U', 'Intel® UHD Graphics 620', 8, 256, 1000, '14.0', 'Lenovo');
	insert into shop_computer values('MacBook', 'Intel Core m3', 'Intel HD Graphics 615', 8, 256, 500, '12.0', 'Apple');
	insert into shop_computer values('MacBook Air', 'Intel Core i5', 'Intel UHD Graphics 617', 8, 256, 500, '13.0', 'Apple');
	insert into shop_computer values('MacBook Pro', 'Intel Core i7', 'Radeon Pro 555X', 16, 512, 1000, '15.0', 'Apple');
	insert into shop_computer values('iMac', 'Intel Core i5', 'Radeon Pro 570', 8, 1024, null, '27.0', 'Apple');
	insert into shop_computer values('Dell G3', 'i5-8300H', 'Nvidia GeForce 1050Ti', 8, 128, 1000, '15.6', 'Dell');
	insert into shop_computer values('XPS 15', 'i7-8705G', 'Radeon™ RX Vega M GL', 16, 512, 2000, '15.6', 'Dell');
	insert into shop_computer values('ALIENWARE M15', 'i7-8750H', 'NVIDIA GeForce GTX 1070 Max-Q', 32, 1024, 2000, '15.6', 'Dell');
	insert into shop_computer values('Latitude 7390', 'i5-8350U', 'Intel® UHD 620', 8, 256, 500, '13.3', 'Dell');
	insert into shop_computer values('Vostro成就15 7000', 'i7-8750H', 'NVIDIA GeForce GTX 1060', 8, 256, 500, '15.6', 'Dell');
	insert into shop_computer values('灵耀S 2代 S4300UN', 'i5-8250U', 'NVIDIA GeForce MX150', 8, 512, 1000, '14.0', 'ASUS');
	insert into shop_computer values('飞行堡垒-FX63VM', 'i7-7700HQ', 'NVIDIA GTX 1060', 8, 128, 1000, '15.6', 'ASUS');
	insert into shop_computer values('A555QG', 'A10-9620P', 'Radeon R5 M430', 4, 256, 500, '15.6', 'ASUS');
	insert into shop_computer values('B8546GD', 'i7-8750H', 'nVidia GeForce GTX 1050', 8, 512, 1000, '15.6', 'ASUS');
	insert into shop_computer values('ROG超神2', 'i7-8750H', 'nVidia GeForce GTX 1080', 32, 512, 1000, '17.3', 'ASUS');
	insert into shop_computer values('VJS112C0811P', 'i5-8250', 'Intel UHD Graphics 620', 16, 1024, 1000, '11.6', 'VAIO');
	insert into shop_computer values('VJS131C11T', 'i7-8550U', 'Intel UHD Graphics 620', 16, 1024, 1000, '13.3', 'VAIO');
	insert into shop_computer values('VJZ131A11T', 'i7-6567U', 'Intel HD Graphics 550', 16, 512, 1000, '13.3', 'VAIO');
commit tran 