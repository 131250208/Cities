
Cities is a simple tool for searching cities located at a given longitude and latitude range. All the cities returned are sorted by the importance of a city and the population density.

# Install
pip install Cities

# Features
1. fast(less than 0.01s for each searching), simple and convenient.
2. cover all the cities around the world.
3. the author is cute.

# Required File
Download  the [city data](https://pan.baidu.com/s/1EPkpZH2pFFR3USGJ5e_gDA) and put it at any directory you want. Remember to set the path up when you initiate an instance.

# Example
```
from Cities import cities_retriever
cr = cities_retriever.CitiesRetriever("Sources/dict_1.json")
cities = cr.retrieve_cities(-124.71, -77.21, 25.24, 44.75, 50) # starting longitude, ending longitude, starting latitude, ending latitude, the number of the cities 
print(json.dumps(cities, indent=2))
```
# Note
it might take you a little time(13s for loading the dict) when you first invoke the retrieve method. But the loading process only occurs when you initiate an instance. The retrieving process is still stay around 0.001s ~ 0.01s(it depends on how many cities you want). The mainly time-consuming part in retrieving is a sorting part. You might wanna load it beforehand instead of loading it when you wanna use it.