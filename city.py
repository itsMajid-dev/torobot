# cookie_of_city:  

AHVAZ         = '537'
ARDEBIL       = '109'
ARAK          = '1125'
BOSHEHR       = '287'
ELLAM         = '265'
KARAJ         = '252'
KHOY          = '67'
MASHHAD       = '468'
OROMIEH       = '66'
SHIRAZ        = '753'
TEHRAN        = '392'
ISFEHAN       = '240'
TABRIZ        = '65'
YAZD          = '1202'
ZANJAN        = '595'
QOM           = '798'
KERMAN        = '825'
KERMAN_SHAH   = '890'
BANDAR_ABBAS  = '1149'
SARI          = '1072'
RAMSAR        = '1087'
HAMEDAN       = '1185'
GORGAN        = '952'







# نحوه یافتن کوکی های هر شهر : 


# import requests 

# for city in range(220 , 1000):
#     c= {
#         '_ga': 'GA1.2.174323781.1727252445',
#         '_ga_CF4KGKM3PG': 'GS1.1.1727259957.3.1.1727265784.60.0.0',
#         '_ga_RXJQRSCLTR': 'GS1.1.1727261890.4.1.1727265784.60.0.0',
#         '_gat_UA-105982196-1': '1',
#         '_gcl_au': '1.1.1936302410.1727252445',
#         '_gid': 'GA1.2.932278947.1727252445',
#         'deliver_city': f'{city}',
#         'display_mode': '',
#         'is_torob_user_logged_in': 'False',
#         'search_session': 'lznfgldjdwdnsdcockbpeysfswxefsay'
#         }
#     url = 'https://api.torob.com/v4/base-product/search/?page=1&sort=popularity&size=24&query=%D9%85%D9%88%D8%B3&shop_type=offline&q=%D9%85%D9%88%D8%B3&source=next_desktop&rank_offset=24&_bt__experiment=&suid=66f6a9abc72d1ad091172eac&_url_referrer='
#     r = requests.get(url , cookies=c )
#     if r.status_code ==200:
#         # try:
#         try:
#             with open("CITY.txt" , '+r' , encoding='utf-8') as f : 
#                 data = f.read()
#                 JJ = r.json()['results'][0]['delivery_city_name']

#                 if JJ in data :
#                     print(JJ)
#                 else:
#                     f.write(f"{JJ} : {city}\n")
#         except:
#             print("ERR ! ")
#         # except:
#         #     print("ERR ! ")