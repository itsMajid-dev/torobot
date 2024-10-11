# torobot

<p align="center">
  <img src="https://github.com/itsMajid-dev/torobot/raw/main/image/main-bg.png" alt="ربات ترب" />
</p>


<p> Search for goods and stores on  <a href="https://torob.com"> torob.com</a>   🍎 </p>


GET START 
=====
```python
import torob
from torob import att
from torob import city
```
**att** : To get a series of attributes of the desired product, we import this package .  
**city** : To specify the city, to bring results related to the city ( default = Tehran)


Product search
=====
Simple search:
```python
a = torob.Search(‘ps5’)
```
A little more precise:
```python
a = torob.Search('ps5',range_price=(20000000 , 35000000) , status='new' )
```
or
```python
a = torob.Search('ps5' , city.MASHHAD , status='stock' ,unknown=True , order='cheap')
```


search parameters:
==
**goods** : The value to search [str]  
**number** : Number of goods received (default 24) [int]  
**page** : search page ( default 0 ) [int]  
**city** : Search city ( default Tehran ) [Select city from ‘city’ module]  
**in_person** : In person (default True ) [bool]  
**status** : Product status (new or stock) ( default None ) [str]  
**order** : Order type (cheap or popular) ( default None ) [str]  
**range_price** : Price range (as a tuple , specifies minimum and maximum price) [tuple]
default = (None , None )  
**unknown** : If it is true, no cookies will be sent by the package to torob.com, so the results will be
different. (default False) [bool]  


initial information
=====
Number of products found :
```python
print(len(a))
```
Product category(ies) :
```python
print(a.categorys)
```
lowest price:
```python
print(a.min_price)
```
most expensive price:
```python
print(a.max_price)
```

More details
=====
Get product images:
=
```python
a.get_images(0)
```
parameter :  
  1- index : Product number (0 to len(a) products have been found)  
Output :  
  Returns a list of product image urls  
  
Get product(s) page url :  
=
```python
a.get_links()
```
output:  
  Returns a list of product addresses  
  
Get information about the product (specifications, descriptions, features):  
=
```python  
a.get_info(0)
```
parameter :  
  1- index : Product number (0 to len(a) products have been found)  
  2-strip: If set to True, it removes extra spaces  
  3- out_put_type: Specifies the type of output (list or string) (default str )  
  4- up_to_page : It repeats this process up to a certain page  

Output:  
  Returns product specifications (as a list or text)  
  
Returns the information of the found products (on current page):  
=
```python
a.get_All(att.NAME_EN ,att.PRICE , only=True ,)
```
parameter :  
  1- args : With the help of the imported att class, get the attribute it needs from the  
  products.  
  2-only : If it is equal to True, it returns as a list and otherwise it returns as a dictionary.  

  3-up_to_page : Returns all product details up to the "up_to_page" page  
Output:  
  The dictionary returns the product specifications of this page  

seller details (phone, location, address):  
=
```python
a.get_seller(1)
```
parameter :  
  1- index : Product number (0 to len(a) products have been found)  
  2-up_to_page : Returns all product details up to the "up_to_page" page  
Output:  
  It returns the contact number, SMS number, store address and location of the seller  


Get related **searches** (similar):  
=
```python
a.get_suggestion()
```
output :  

  return list of suggestion  

Goods in other stores:  -
=
```python
a.get_more_store(0)
```
parameter :  
  1- index : Product number (0 to len(a) products have been found)  
Output:  
  It returns the specifications of similar products in other stores.  
  
Returns the specifications of similar **products**:  
=
```python
a.get_similar(0 , short=True)
```
parameter :  
  1- index : Product number (0 to len(a) products have been found)  
  2- short: If it is True; Shows the output more concisely  
Output :  
  Returns a dictionary of similar products (containing the name, price, city and address of
  the product photo )  
 

