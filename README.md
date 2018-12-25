Cities is a simple tool for searching cities located at a given longitude and latitude range or a given region(country, state, province). 
All the cities returned are sorted by the importance of a city and the population density.

# Install
```commandline
pip install Cities
```

# Features
1. fast(less than 0.01s for each retrieving), simple and convenient.
2. cover all the cities around the world.
3. the author is cute.

# Required File
Download  the [city data](https://pan.baidu.com/s/10qjtq9jl7tLxXeypfJCrEg) and put it at any directory you want. Remember to set the path up when you initiate an instance.

# Example
```python
from Cities import cities_retriever

cr = cities_retriever.CitiesRetrieverByRect("Sources/dict_2.json")
cities = cr.retrieve_cities(lon_start=-124.71, lon_end=-77.21, lat_start=25.24, lat_end=44.75, num=500) # num is optional, default: 999999
print(cities)
print(len(cities))

cr = cities_retriever.CitiesRetrieverByRegionName("Sources/dict_region2cities.json")
cities = cr.retrieve_cities(country="United States", region="Washington", num=500) # region and num are optional
print(cities)
print(len(cities))
```
# Note
the bigger the dict file is, the longer the loading time is.
## 4million cities --- 12s
1. dict_all_cities_region2cities.json
2. dict_all_cities_rect2cities.json
## 8000 cities --- < 1s
1. dict_cities_8000_region2cities.json
2. dict_cities_8000_rect2cities.json