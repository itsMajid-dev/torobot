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
