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
-
```python
a.get_images(0)
```
parameter :  
  1- index : Product number (0 to len(a) products have been found)  
Output :  
  Returns a list of product image urls  
  
Get product(s) page url :  
-
```python
a.get_links()
```
output:  
  Returns a list of product addresses  
  
Get information about the product (specifications, descriptions, features):  
-
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
-
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
-
```python
a.get_seller(1)
```
parameter :  
  1- index : Product number (0 to len(a) products have been found)  
  2-up_to_page : Returns all product details up to the "up_to_page" page  
Output:  
  It returns the contact number, SMS number, store address and location of the seller  


Get related **searches** (similar):  
-
```python
a.get_suggestion()
```
output :  

  return list of suggestion  

Goods in other stores:  -
-
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
 
save products information
=====

```python
a.save(att.PRICE , att.NAME_FA , formating='excel'
,add_row=True , add_info=True , replaced='ناموجود')
```
parameters:
1-args: With the help of the imported att class, get the attribute it needs from the
products
2-up_to_page : Returns all product details up to the "up_to_page" page
3-formating : Specifies the saved format, it can be equal to the following:
A) 'excel' or 'xlsx' or 'xls' or 'e' = To save as Excel

B) 'xml' or 'x' = To save as XML
C) 'sql' or 'db' or 's' = To save as SQL
D) 'html' or 'h' or 'table' or 'htm' = To save as HTML
E) 'str' or 'txt' or 'text' or 'string' = To save as TEXT
F) 'hdf5' or 'h5' = To save as HD5
G) 'feather ' or 'pandas' or 'f' = To save as PANDAS format
H) 'json' or 'j' = To save as JSON
I) 'csv' or 'c' or 'csvx' = To save as CSV
4-replaced : If the product does not have this feature, it replaces this value in the output
file (default "-")
5-file_name : Output file name
6-add_info : If it is True, it will add product details to the file with the help of the
get_info method (default False)
7- add_row : If it is True, it puts one row (one number) for each product


Get store information
=====

Get 3 stores whose names include "پارس". :
-
```python
c = torob.Shop(name='پارس' , count=3)
```
parameters:
1-name: The name of the desired store
2- count : Number of stores received

Getting store information:
-
```python
print(c.get_information())
```
Getting the number of stores that have the same name:
-
```python
print(c.get_count())
```

Get address of the store:
-
```python
print(c.get_address(2))
```
parameters:
1-index: Which store? store index (from 0 to count-1) can be

Returns store's performance score:
-
```python
print(c.get_score(1))
```
parameters:
1-index: Which store? store index (from 0 to count-1) can be

Returns the store's permissions and credentials:
-
```python
print(c.get_license(1))
```

Returns the cooperation history of the store:
-
```python
print(c.get_history(1))
```





<p style='text-align: center;'> <b><a href='https://github.com/itsMajid-dev/torobot/blob/main/torobot_documentation.pdf'>more documentation</a></b></p>



