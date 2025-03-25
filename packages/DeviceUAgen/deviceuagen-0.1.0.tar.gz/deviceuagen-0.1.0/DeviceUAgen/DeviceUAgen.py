import random, subprocess

class DeviceCatalog:
	
	def generate_model(Jar):
		return {
			"Realme": ["Realme 12 Pro", "Realme GT Neo 6", "Realme C67", "Realme Narzo 60","Realme 10 Pro+", "Realme GT 5", "Realme 9i", "Realme C55", "Realme Narzo 50","Realme 8 Pro", "Realme X7 Max", "Realme C35", "Realme Narzo 30", "Realme GT Neo 5","Realme GT 2 Pro", "Realme 7", "Realme X50 Pro", "Realme C25s", "Realme 6 Pro"],
			"Samsung": ["SM-A135F","Galaxy S23 FE", "Galaxy A34", "Galaxy Z Flip5", "Galaxy M14 5G", "Galaxy S22","Galaxy A14", "Galaxy M13", "Galaxy F23 5G", "Galaxy Z Fold4", "Galaxy S21 Ultra","Galaxy Note 20 Ultra", "Galaxy A73", "Galaxy Xcover 6 Pro", "Galaxy S20 FE","Galaxy A52s 5G","SM-A135F", "Galaxy S24 Ultra", "Galaxy Z Fold5", "Galaxy A54", "Galaxy M14"],
			"Oppo": ["CPH2591","CPH2591", "Oppo Find X7 Pro", "Oppo Reno 11", "Oppo A98", "Oppo K11","Oppo Find N3 Flip", "Oppo A78", "Oppo F23", "Oppo Reno 8T", "Oppo Reno 7","Oppo K10", "Oppo A58", "Oppo Find X5 Pro", "Oppo Reno 6 Pro", "Oppo A17","Oppo Find X3 Pro", "Oppo A55", "Oppo F19 Pro", "Oppo Reno 5", "Oppo A16K"],
			"Vivo": ["Vivo X100 Pro", "Vivo V30", "Vivo Y200", "Vivo T2 5G","Vivo X100 Pro", "Vivo V30", "Vivo Y200", "Vivo T2 5G", "Vivo X90s","Vivo iQOO 12", "Vivo Y78", "Vivo V27", "Vivo Y16", "Vivo iQOO Neo 7","Vivo X80 Pro", "Vivo Y33s", "Vivo V25 Pro", "Vivo Y21", "Vivo X70 Pro+","Vivo V21", "Vivo Y12s", "Vivo T1 5G", "Vivo X60", "Vivo iQOO 9 Pro"],
			"Huawei": ["Huawei P70 Pro", "Huawei Mate 60", "Huawei Nova 12", "Huawei Enjoy 70","Huawei P70 Pro", "Huawei Mate 60", "Huawei Nova 12", "Huawei Enjoy 70","Huawei P60", "Huawei Mate X5", "Huawei Y9a", "Huawei Nova 11i", "Huawei P50 Pocket","Huawei Mate 50 Pro", "Huawei P40", "Huawei Y7a", "Huawei Nova 9", "Huawei Mate X3","Huawei P30 Pro", "Huawei Y6p", "Huawei Mate 40", "Huawei Nova 7", "Huawei Enjoy 20"],
			"Google": ["Pixel 9 Pro", "Pixel 8a", "Pixel 7", "Pixel Fold 2","Pixel 9 Pro", "Pixel 8a", "Pixel 7", "Pixel Fold 2", "Pixel 6a","Pixel Tablet", "Pixel 5", "Pixel 4a", "Pixel 3 XL", "Pixel 2 XL","Pixel 6 Pro", "Pixel 5a", "Pixel 4", "Pixel 3a", "Pixel Slate"],
			"Xiaomi": ["23053RN02A", "22111317PG","23053RN02A", "22111317PG", "Xiaomi 14 Ultra", "Redmi Note 13 Pro", "Poco F5","Black Shark 5 Pro", "Xiaomi 13T Pro", "Redmi K60", "Poco X5 Pro", "Xiaomi Pad 6","Xiaomi Mi 11 Ultra", "Redmi Note 12", "Poco F4 GT", "Black Shark 4", "Redmi 10C","Xiaomi 12 Pro", "Poco M4 Pro", "Xiaomi Mi Mix Fold", "Redmi K40", "Xiaomi Mi 10T Pro"],
			"OnePlus": ["OnePlus 12", "OnePlus 11R", "OnePlus Nord 3", "OnePlus 10 Pro", "OnePlus Ace 2","OnePlus 9 Pro", "OnePlus 8T", "OnePlus Nord CE 2", "OnePlus 7T", "OnePlus 6"],
			"Sony": ["Xperia 1 V", "Xperia 5 V", "Xperia 10 IV", "Xperia Pro-I","Xperia 1 III", "Xperia 5 III", "Xperia 10 III", "Xperia XZ2", "Xperia Z5"],
			"Motorola": ["Moto G84", "Moto Edge 40", "Moto Razr 40 Ultra", "Moto G73","Moto G200", "Moto Edge 30 Pro", "Moto G60", "Moto Razr 2022", "Moto G100"],
			"Nothing": ["Nothing Phone (2)", "Nothing Phone (1)"],
			"Asus": ["ROG Phone 8", "Zenfone 10", "ROG Phone 7", "Zenfone 9", "ROG Phone 6D"],
			"Lenovo": ["Lenovo Legion Phone Duel 2", "Lenovo Tab P12 Pro", "Lenovo K13", "Lenovo Z6 Pro"],
			"Nokia": ["Nokia X30 5G", "Nokia G60", "Nokia C32", "Nokia XR20", "Nokia 5.4"],
			"ZTE": ["ZTE Axon 50 Ultra", "ZTE Nubia Red Magic 8 Pro", "ZTE Blade V40", "ZTE Axon 40 Ultra"],
			"Honor": ["Honor Magic6 Pro", "Honor 90", "Honor X50", "Honor Play 40", "Honor Magic5 Ultimate"],
			"Meizu": ["Meizu 20 Pro", "Meizu 18s", "Meizu 16T", "Meizu M10", "Meizu 15 Plus"],
			"Infinix": ["Infinix Zero 30", "Infinix Note 30", "Infinix Smart 8", "Infinix GT 10 Pro"],
			"Tecno": ["Tecno Phantom X2 Pro", "Tecno Camon 20", "Tecno Pova 5 Pro", "Tecno Spark 10"],
		}

class GenerateUseragent:
	
	os_ver = {'9': 'PPR1', '10': 'QP1A', '11': 'RP1A', '12': 'SP1A', '13': 'TP1A', '14': 'UP1A'}
	
	def __init__(Jar):
		Jar.brand = DeviceCatalog().generate_model()
		Jar.model_list = list(Jar.brand.keys())
	
	def versi_chrome(Jar):
		return f'{random.randrange(100, 133)}.0.{random.randrange(4200, 6900)}.{random.randrange(40, 190)}'
		
	def android_version(Jar, android_version):
		return Jar.os_ver.get(str(android_version), 'AP4A')
		
	def get_device(Jar, brand=None, system=False):
		if system:return Jar.get_system_device()
		if not brand or brand not in Jar.brand:
			brand = random.choice(Jar.model_list)
		model = random.choice(Jar.brand[brand])
		android = random.choice(['9', '10', '11', '12', '13', '14', '15'])
		build_code = Jar.android_version(android)
		build =f"{build_code}.{random.randint(211111, 233333)}.00{random.randint(1, 9)}"
		return {"model": model, 'android': android, 'chrome': Jar.versi_chrome(), 'build': build}
	
	def get_system_device(Jar):
		try:
			model = subprocess.check_output("getprop ro.product.model", shell=True).decode().strip()
			android = subprocess.check_output("getprop ro.build.version.release", shell=True).decode().strip()
			build = subprocess.check_output("getprop ro.product.build.id", shell=True).decode().strip()
			if not model or not android or not build:
				Jar.get_device()
			return {"model": model, 'android': android, 'chrome': Jar.versi_chrome(), 'build': build}
		except Exception:
			Jar.get_device()
	
	def get_device_2(Jar, brand=None, system=False):
		if system:return Jar.get_system_dalvik()
		if not brand or brand not in Jar.brand:
			brand = random.choice(Jar.model_list)
		model = random.choice(Jar.brand[brand])
		android = random.choice(['9', '10', '11', '12', '13', '14', '15'])
		simcard = random.choice(['Telkomsel', 'XL Axiata', 'Indosat', 'Smartfren', 'Tri'])
		return {'brand': brand, 'brand2': brand,'model': model, 'android': android, 'cpu': 'arm64-v8a', 'simcard': simcard}
		
	
	def get_system_dalvik(Jar):
		try:
			brand = subprocess.check_output("getprop ro.product.manufacturer", shell=True).decode().strip()
			brand2 = subprocess.check_output("getprop ro.product.brand", shell=True).decode().strip()
			model = subprocess.check_output("getprop ro.product.model", shell=True).decode().strip()
			android = subprocess.check_output("getprop ro.build.version.release", shell=True).decode().strip()
			simcard = subprocess.check_output('getprop gsm.operator.alpha', shell=True).decode().strip().split(",")[1].replace("\n","")
			cpu = subprocess.check_output("getprop ro.product.cpu.abi", shell=True).decode().strip()
			if not model or not android or not cpu:
				Jar.get_device_2()
			return {'brand': brand, 'brand2': brand2, 'model': model, 'android': android, 'cpu': cpu, 'simcard': simcard}
		except Exception:
			Jar.get_device_2()
	
	def useragent(Jar, brand=None, system=False, dalvik=False):
		density, width, height = round(random.uniform(1.0, 4.0), 2), random.randint(720, 1440), random.randint(1280, 2560)
		
		if dalvik:
			device_info = Jar.get_device_2(brand, system)
			brand, brand2, model, android, cpu, simcard = device_info.values()
			return f'[FBAN/FB4A;FBAV/486.0.0.66.70;FBBV/653066364;FBDM/{{density={density},width={width},height={height}}};FBLC/id_ID;FBRV/0;FBCR/{simcard};FBMF/{brand};FBBD/{brand2};FBPN/com.facebook.katana;FBDV/{model};FBSV/{android};FBOP/1;FBCA/{cpu}:;]'
		else:
			device_info = Jar.get_device(brand, system)
			model, android, chrome, build = device_info.values()
			return f'Mozilla/5.0 (Linux; Android {android}; {model} Build/{build}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome} Mobile Safari/537.36'
		
if __name__ == "__main__":
    os = GenerateUseragent()