import requests 
import pandas 
from typing import Literal, Optional
from . import att
from . import city  
from bs4 import BeautifulSoup  as Bot 
import re
from string import ascii_uppercase 


class FormatingError(Exception):
    pass

class NetW(Exception):
    pass

class NoInternet(Exception):
    pass


class Search:
    """Search
    =====
    Product search on torob.com ✨
    """
    def __init__(self ,
                goods:str,
                number:int =100,
                page:int=0,
                city:str=city.TEHRAN , 
                in_person:bool=True,
                status:Optional[Literal['stock', 'new']] = None,
                order : Optional[Literal['popular', 'cheap']] = None,
                range_price:tuple = (None, None),
                unknown:bool=False , 
                ) :
        
        if range_price != (None , None):
            if isinstance(range_price , tuple):
                self.range =  f'&price__gt={range_price[0]}&price__lt={range_price[1]}'
            else:
                self.range =  f'&price__gt=0&price__lt={range_price}'

        else:
            self.range = ''

        self.unknown = unknown
        self.all_goods = None
        self.max_price = None
        self.min_price = None
        self.categorys = None
        self.__data = None
        self.city = city
        self.goods = f'&query={goods.replace(" " , "+")}'.strip()
        self.number = f'&size={number}'.strip() 
        self.page = str(page).strip()
        self.in_person = '&shop_type=offline' if in_person==True else '&shop_type=online' 
        self.status = f'&stock_status={status}'.strip() if status != None else ''
        self.order = f'&sort=price' if order == 'cheap'.strip() else '&sort=popularity'
        requests.session()
        self.__url = f'https://api.torob.com/v4/base-product/search/?page={self.page}{self.order}{self.number}{self.goods}&available=true{self.in_person}{self.status}{self.range}&q={goods.replace(" " , "+")}&source=next_desktop'
        
        
        
        self.cookies = {
                '_ga': 'GA1.2.174323781.1727252445',
                '_ga_CF4KGKM3PG': 'GS1.1.1727259957.3.1.1727265784.60.0.0',
                '_ga_RXJQRSCLTR': 'GS1.1.1727261890.4.1.1727265784.60.0.0',
                '_gat_UA-105982196-1': '1',
                '_gcl_au': '1.1.1936302410.1727252445',
                '_gid': 'GA1.2.932278947.1727252445',
                'deliver_city': f'{city}',
                'display_mode': '',
                'is_torob_user_logged_in': 'False',
                'search_session': 'lznfgldjdwdnsdcockbpeysfswxefsay'
                }
        self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x68) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept': 'application/json',
            }
        try: 
            if not unknown:
                request = requests.get(self.__url , cookies=self.cookies , headers=self.headers)
            else :
                request = requests.get(self.__url  , headers=self.headers)

            self.__data = request.json()
            self.all_goods = self.__data['count']
            self.max_price = (self.__data['max_price'] , 'TIR')
            self.min_price = (self.__data['min_price'] , 'TIR')
            self.categorys = [title['title'] for title in self.__data['categories']]

        except requests.exceptions.ConnectionError as E : 
            return E
            # raise requests.exceptions.ConnectionError("FUUUUUUUUUC")
    def __len__(self):
        
        return len(self.__data['results'])
    
    def __call__(self, *args  , goods_limit=(0,1) , ):
        list_key_value_per = []
        for j in self.get_All(*args , only=True):
            list_key_value_per.append((j))
            
        return list_key_value_per[goods_limit[0]:goods_limit[1]+1]

    def __str__(self):
        return f"Search for {self.goods.split('=')[1]} on torob.com"
    

    def get_All(self , *args , only=False , up_to_page=None):
        """
    **Returns the information of the found products in the form of a `dict`**

In the delivered dictionary:
- **key**: Name of the searched product
- **value**: A list of features that you specified to be retrieved from the product

Inputs:
1. **args**:  
   First, import the `att` module as follows:
   ```python
   from torob import att
   ```
   Then use the `att` variables to retrieve the desired product attributes.

For example:
If I want to return the price and the English name of the product(s):
```python
a = torob.Search('موس')
print(a.get_All(att.NAME_EN, att.PRICE))
```

For more formatted output:
```python
for i, j in a.get_All(att.NAME_EN, att.PRICE).items():
    print(i, j, sep=': ')
```
2. **up_to_page**:
Returns all product details up to page **up_to_page**

3. **only**:
This parameter returns only the specified atts in list format,

example out put:

```
['Green GM606-RGB Gaming Mouse', 660000]
['Logitech G G304 Lightspeed Gaming Mouse', 315000]
['MOUSE A4TECH GAMING BLOODY A60', 1960000]
['TSCO TM 286 Mouse', 165000]
['', 369000]
['TSCO TM 2021 Gaming Mouse', 330000]
```
...
"""
        def goto(number):
            new_url = self.__url.replace(f'page={self.page}' , f'page={number}')
            return new_url 
        
        def fetch_json(url , auth=self.unknown):
            if auth:
                req = requests.get(url)
            else:
                req = requests.get(url , cookies=self.cookies, headers=self.headers)
            try:
                return req.json()
            except:
                return None
        
        if isinstance(up_to_page , int) : 
            goods      = {}
            goods_only = []
            for u in range(up_to_page+1):
                new = goto(number=u)
                if not self.unknown:
                    req = requests.get(new , cookies=self.cookies, headers=self.headers)
                else:
                    req = requests.get(new ,)

                new_data = req.json()
                for g in range(len(new_data['results'])):
                    list_of_atts = list()
                    gd = []
                    for a in args:
                        if a == att.CITY:
                            try:
                                list_of_atts.append(new_data['results'][g]['delivery_city_name'])
                            except:
                                list_of_atts.append('unknown')
                        elif a==att.PHONE:
                            api_1 = new_data['results'][g]['more_info_url']
                            api_2=fetch_json(api_1)['new_buy_box_contact_url']
                            if api_2:
                                api_3 = fetch_json(api_2)['phone']
                            else:
                                api_3 = None
                            list_of_atts.append(api_3)

                        elif a==att.ADDRESS:
                            api_1 = new_data['results'][g]['more_info_url']
                            api_2=fetch_json(api_1)['new_buy_box_contact_url']
                            if api_2:
                                api_3 = fetch_json(api_2)['address']
                            else:
                                api_3 = None
                            list_of_atts.append(api_3)

                        else:       
                            list_of_atts.append(new_data['results'][g][a])
                            
                        goods[f"{u}{g}"] =  list_of_atts
                        if a not in [att.PHONE , att.ADDRESS]:
                            gd.append(new_data['results'][g][a])
                        else:
                            gd.append(api_3)
                        
                    goods_only.append(gd)

            if not only:
                return goods
            else:
                return goods_only
        else:
            goods = {}
            goods_only = []
            for g in range(len(self.__data['results'])) :  
                list_of_atts = list()
                gd = []
                for a in args:
                    if a == att.CITY:
                        list_of_atts.append(self.__data['results'][g]['delivery_city_name'])
                    elif a==att.PHONE:
                        api_1 = self.__data['results'][g]['more_info_url']
                        api_2=fetch_json(api_1)['new_buy_box_contact_url']
                        
                        if api_2:
                            api_3 = fetch_json(api_2)['phone']
                        else:
                            api_3 = None
                        list_of_atts.append(api_3)

                    elif a==att.ADDRESS:
                        api_1 = self.__data['results'][g]['more_info_url']
                        api_2=fetch_json(api_1)['new_buy_box_contact_url']
                        
                        if api_2:
                            api_3 = fetch_json(api_2)['address']
                        else:
                            api_3 = None
                        list_of_atts.append(api_3)
                    else:
                        list_of_atts.append(self.__data['results'][g][a] )
                    goods[g] =  list_of_atts
                    if a not in [att.PHONE , att.ADDRESS]:
                        gd.append(self.__data['results'][g][a])
                    else:
                        gd.append(api_3)
                goods_only.append(gd)

            if not only:
                # pass
                return goods
            else:
                # pass
                return goods_only
            
    
    
    def get_images(self , index:int):
        """
        Returns all images of the selected product in the form of a list
        Inputs:  
        1- **index**: Enter the product number ( 0 to len(Search()) )  
        """
        data_of_goods = self.__data['results'][index]['media_urls']
        list_of_image = list()
        for i in range(len(data_of_goods)):
            img = data_of_goods[i]['url']
            list_of_image.append(img)
        return list_of_image
    

    def get_links(self , ):
        """
    Returns the URL of the page containing all found products or the API endpoint for all products in the form of a list
            """
        links = []
        for l in range(len(self.__data['results'])):
            base_url = 'https://torob.com'
            links.append(f"{base_url}{self.__data['results'][l]['web_client_absolute_url']}")
        return links

    def get_info(self , index:int , strip=False ,up_to_page=None , out_put_type:Optional[Literal['str', 'list']] = 'str'):
        """
        Return product information  
        Inputs:  
        1- **index**: Enter the product number (0 to len(Search())  
        2- **strip**: If set to True, it removes extra spaces  
        3- **out_put_type**: Specifies the type of output (list or string)."""

        list_of_informations = []
        if isinstance(up_to_page , int):
            def goto(number):
                new_url = self.__url.replace(f'page={self.page}' , f'page={number}')
                return new_url 
            for u in range(up_to_page):
                new = goto(number=u)

                if not self.unknown:
                    req = requests.get(new , cookies=self.cookies, headers=self.headers)
                else:
                    req = requests.get(new ,)
               
                url_goods = req.json()['results'][index]['web_client_absolute_url']
                html = requests.get(f"https://torob.com{url_goods}").text
                bot = Bot(html , 'html.parser')
                data = bot.select(".product-section")  # more select :  .specs-content   ,   .jsx-d9bfdb7eefd5a6bf ,
                f= open("data.txt" , 'w' , encoding='utf-8')
                for i in range( 1 , len(data) ,1 ):  # step3 : title
                    # text = re.sub(r'[.,]', ' ', f"\n{data[i].get_text(separator='\n' , strip=True , )}\n") == Err!
                    text = re.sub(r'[.,]', ' ', "\n{}\n".format(data[i].get_text(separator='\n', strip=strip)))
                    list_of_informations.append(text)
                    f.write(text)

            if out_put_type == 'str':
                return ''.join(list_of_informations)
            elif out_put_type =='list':
                return list_of_informations
        else:
            url_goods = self.__data['results'][index]['web_client_absolute_url']
        html = requests.get(f"https://torob.com{url_goods}").text
        bot = Bot(html , 'html.parser')
        data = bot.select(".product-section")  # more select :  .specs-content   ,   .jsx-d9bfdb7eefd5a6bf ,
        f= open("data.txt" , 'w' , encoding='utf-8')
        for i in range( 1 , len(data) ,1 ):  # step3 : title
            # text = re.sub(r'[.,]', ' ', f"\n{data[i].get_text(separator='\n' , strip=True , )}\n") == Err!
            text = re.sub(r'[.,]', ' ', "\n{}\n".format(data[i].get_text(separator='\n', strip=strip)))
            list_of_informations.append(text)
            f.write(text)

        if out_put_type == 'str':
            return ''.join(list_of_informations)
        elif out_put_type == "list":
            return list_of_informations
        
    def get_more_store(self , index:int):
        """Product in **other** stores"""
        s = {}
        target = self.__data['results'][index]['more_info_url']
        if self.unknown:
            data = requests.get(target).json()
        else:
            data = requests.get( target, cookies=self.cookies, headers=self.headers).json()

        number_of_store = data['products_info']['count']
        # headers = ascii_uppercase[0:number_of_store+1]
        headers = [i  for i in  range(0,number_of_store) ]
        for store , head in zip(range(0 , number_of_store) , headers):
            d={}
            stores = data['products_info']['result'][store]
            d['store_name'] = stores['shop_name']
            d['store_location'] = stores['shop_name2']
            d['store_score'] =stores['shop_score']
            d['price_in_store'] = stores['price']
            d['name_in_store'] = stores['name1']
            s[f'{head}']= d
         
        return s
        
    
    def get_seller(self, index:int, up_to_page=None):
        """Returns **seller** details (phone, location, address) as a dictionary."""
        
        def fetch_json(url, use_auth=self.unknown):
            req = requests.get(url,) if use_auth else requests.get(url,cookies=self.cookies, headers=self.headers)
            return req.json()

        def get_value(data, key):
            try:
                return data[key]
            except KeyError:
                return None

        def process_seller(api_goods_url):
            seller_info = {}
            try:
                cnc_url = fetch_json(api_goods_url)['new_buy_box_contact_url']
                information = fetch_json(cnc_url, use_auth= not self.unknown)
                seller_info = {
                    'phone': get_value(information, 'phone'),
                    'address': get_value(information, 'address'),
                    'messenger': get_value(information, 'messenger_phone'),
                    'location': get_value(information, 'coordinates')
                }
            except Exception:
                seller_info = {'phone': None, 'address': None, 'messenger': None, 'location': None}
            
            return seller_info
        
        specifications = {}
        
        if isinstance(up_to_page, int):
            def build_url(page):
                
                return self.__url.replace(f'page={self.page}', f'page={page}')

            for page in range(0, up_to_page + 1):
                new_url = build_url(page)
                data = fetch_json(new_url, use_auth=not self.unknown)
                api_goods = data['results'][index]['more_info_url']
                specifications[f'seller_{page}'] = process_seller(api_goods)

            return specifications

        api_goods = self.__data['results'][index]['more_info_url']
        specifications['seller'] = process_seller(api_goods)

        return specifications
        # return specifications

        
    def get_similar(self , index:int  , short=False ):
        """
        Returns similar products in the form of a list

        Inputs:  
        1- **index**: Enter the product number (0 to len(Search()) )  
        2- **short**:  If it is True; Shows the output more concisely    

        """
        dict_of_similar = dict()

        url_goods = self.__data['results'][index]['similar_api']
        if self.unknown:
            request = requests.get(url_goods)
        else:
            request = requests.get(url_goods ,cookies=self.cookies, headers=self.headers )
        
        data = request.json()
        number_of_similar = len(data['results'])
        if number_of_similar<=26:
            header = ascii_uppercase[0:number_of_similar]
        else:
            header = [i  for i in  range(0,number_of_similar+1) ]
        
        for s,h in zip(range(0 , number_of_similar) , header):
            get_info = data['results'][s]
            if short:
                dict_of_similar[h] = (get_info['name1'], get_info['name2'], get_info['price'], get_info['image_url'])
            else:
                dict_of_similar[h] = (['name_fa', get_info['name1']] , ['name_en',get_info['name2']] , ['price',get_info['price']],['image',get_info['image_url']])


        return dict_of_similar

        # روش دوم : 

        # list_of_similar = list()
        # url_goods = self.__data['results'][index]['web_client_absolute_url']
        # html = requests.get(f"https://torob.com{url_goods}").text
        # bot = Bot(html , 'html.parser')
        # data = bot.select(".product-name") # more class =  .detail-value  , .sub-sectio  , 
        # for i in range(len(data)):
        #     list_of_similar.append('\n{}\n'.format(data[i].get_text(separator='\n', strip=True)))
            

        # return list_of_similar
    
    def get_suggestion(self) -> set :
        """ return list of suggestion. """

        list_of_suggestion=set()
        request = requests.get(f"https://api.torob.com/suggestion2/?q={self.goods.split('=')[1]}")
        for s in request.json():
            suggestion = s['text']
            list_of_suggestion.add(suggestion)
            
        return list_of_suggestion
    

    def get_info_2(self , index):
        """return informations (type two)"""

        if self.unknown:
            req = requests.get(self.__data['results'][index]['more_info_url'])
        else:
            req = requests.get(self.__data['results'][index]['more_info_url'] , cookies=self.cookies, headers=self.headers )

        data = req.json()['structural_specs']
        return data
            


    def save( self, *args,
            up_to_page=None ,
            formating='e',
            replaced='-',
            file_name='Torob',
            add_info=False,
            add_row =True,
             ):
        """The extracted data is saved as Excel, XML, json, sql,

        ```
        ['xls' , 'xml' , 'json' , 'db' , 'html' , 'h5' , 'pandas' , 'txt' , 'csv']

        """
        data = self.get_All(*args , only=True , up_to_page=up_to_page)
        dict_format_in_save = {}
        indexed_list        = []
        lis_of_info         = []
        status = 'not saved!'

        if add_info:
            for i in range(0,len(data)):
                lis_of_info.append("".join(self.get_info(index=i)).replace("\n" , '.'))
            indexed_list.append(lis_of_info)

        if isinstance(data , list):
            for DATA in range(0 , len(args)):
                attributes = []
                for a in data :
                    try:
                        attributes.append(a[DATA])
                    except IndexError :
                        attributes.append(replaced)
                indexed_list.append(attributes)
        
            def add_row_in_dict():
                row = []
                for R in range(1, len(data)+1):
                    row.append(R)
                indexed_list.append(row)

        if add_row:
            add_row_in_dict()
        if len(indexed_list)<=26:
            header = ascii_uppercase[0:len(indexed_list)]
        else:
            header = [i  for i in  range(0,len(indexed_list)) ]

        char_waste = ['None', None, 'none', '  ' , ' ' , '-'  , '']
        indexed_list =[[replaced if i in char_waste else i  for i in y] for y in indexed_list ]

        for h,i in zip(header , indexed_list):   
            dict_format_in_save[h] = i
           
        try:
            df = pandas.DataFrame(dict_format_in_save)
            if formating.strip().lower() in ['excel' , 'xlsx' , 'xls' ,'e' ] :
                df.to_excel(f"{file_name}.xlsx" , sheet_name=file_name ,index=False )
                status = 'saved'

            elif formating.strip().lower() in ['xml' , 'x' ] :
                df.to_xml(f"{file_name}.xml"  ,index=False )
                status = 'saved'

            elif formating.strip().lower() in ['sql' , 's' ,'db'] :
                df.to_sql(f"{file_name}.db"  ,index=False )
                status = 'saved'

            elif formating.strip().lower() in ['csv' , 'c' , 'csvx'  ] :
                df.to_csv(f"{file_name}.csv" ,  index=False )
                status = 'saved'
            
            elif formating.strip().lower() in ['html' , 'h' , 'htm' , 'table' ] :
                df.to_html(f"{file_name}.html" ,  index=False )
                status = 'saved'
            
            elif formating.strip().lower() in ['json' , 'j' ] :
                df.to_json(f"{file_name}.json" ,  index=False  , indent=4 , )
                status = 'saved'

            elif formating.strip().lower() in ['feather' , 'f'  , 'pandas'] :
                df.to_feather(f"{file_name}.feather" , )
                status = 'saved'

            elif formating.strip().lower() in ['hdf5' , 'h5' ] :
                df.to_hdf(f"{file_name}.h5" ,index=False )
                status = 'saved'

            elif formating.strip().lower() in ['string' , 'str' , 'txt' , 'text'] :
                df.to_string(f"{file_name}.txt" ,index=False )
                status = 'saved'
            else:
                raise FormatingError("The entered format is invalid,")
        except:
            pass
            # It tries to save the data, there is no need to handle the error!
        return status
            


class Shop:
    """Shop
=====
Getting information about stores registered on torob.com✨
"""


    def __init__(self , name:str ,count ):
        def header(n):
            row = []
            for i in range(0 , n):
                row.append(i)
            return row
        self.name = name.replace(" " , '+')
        self.count = count

        if isinstance(count,int):
            self.number = count
            self.head = header(self.number)
            self.__address = f'https://api.torob.com/v4/internet-shop/list/?page=0&q={self.name}&size={self.number}&show_blocks=true&shop_type=all'
            self.min_range = 0
            self.max_range = self.number

        elif isinstance(count , tuple):
            self.number = (self.count[0] , self.count[1])
            self.head = header(self.number[1])
            self.__address = f'https://api.torob.com/v4/internet-shop/list/?page=0&q={self.name}&size={self.number[1]}&show_blocks=true&shop_type=all'
            self.min_range = self.number[0]
            self.max_range = self.number[1]
        else:
            raise FormatingError('The count parameter can be "number" or "tuple".')
       

    def get_count(self):
        """Number of stores found"""
        
        self.__address = f'https://api.torob.com/v4/internet-shop/list/?page=0&q={self.name}&size=30000&show_blocks=true&shop_type=all'
        try:
            request = requests.get(self.__address)
            data = request.json()
            return data['count']
        except requests.exceptions.ConnectionError as e :
            raise NoInternet(e)


    def get_information(self):
        """return name , logo , website , type and city  of shop"""
        info = {}
        for  head, shop in zip(self.head , range(self.min_range , self.max_range)):
            request = requests.get(self.__address)
            data = request.json()['results'][shop]
            
            list_of_information = {
            'name' : data['name'],
            "site" : data['domain'],
            'logo' : data['shop_logo'],
            'city' : data['city'],
            'type' : data['shop_type'],
            'id' : data['id'],
            }
            
            info[int(head)] = list_of_information
        return info
    
    def get_license(self , index, ):
        """Returns the store's permissions and credentials"""

        id_= self.get_information()[index]['id']
        url = f'https://torob.com/shop/{id_}/'
        request = requests.get(url)
        data = request.text
        bot = Bot(data , 'html.parser')
        follow_up = bot.select(".sub-section:nth-child(1) .property-value") #.property-value
        for f in follow_up:
            return f.get_text(strip=True , separator='\n')

    def get_history(self , index:int=0):
        """Returns the cooperation history of the store"""

        id_= self.get_information()[index]['id']
        url = f'https://torob.com/shop/{id_}/'
        request = requests.get(url)
        data = request.text
        bot = Bot(data , 'html.parser')
        follow_up = bot.select(".sub-section:nth-child(2) .property-value") #.property-value
        for f in follow_up:
            return f.get_text(strip=True , separator='\n')

    def get_address(self , index:int=0):
        'Returns the address of the store'

        id_= self.get_information()[index]['id']
        url = f'https://torob.com/shop/{id_}/'
        request = requests.get(url)
        data = request.text
        bot = Bot(data , 'html.parser')
        follow_up = bot.select(".sub-section:nth-child(8) .property-value") #.property-value
        for f in follow_up:
            return f.get_text(strip=True , separator='\n')
        
    def get_score(self , index:int=0):
        """Returns the store's performance score"""

        id_= self.get_information()[index]['id']
        url = f'https://torob.com/shop/{id_}/'
        request = requests.get(url)
        data = request.text
        bot = Bot(data , 'html.parser')
        follow_up = bot.select(".sub-section:nth-child(3) .property-value") #.property-value
        for f in follow_up:
            return f.get_text(strip=True , separator='\n')


        