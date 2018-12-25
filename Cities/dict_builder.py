import json
import logging
import pyprind
import math
from Cities import settings
from itertools import islice
import csv
import numpy as np
import re


def build_dict_region2cities(raw_data_path, cities_range=None):
    '''

    :param raw_data_path:
    :param cities_range: only consider cities in the range
    :return:
    '''

    dict_region2cities = {}
    prog = pyprind.ProgBar(4181951)
    logging.warning("start building dict region2cities...")
    with open(raw_data_path, 'r', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in islice(reader, 1, None):
            city_name = row[0]
            if cities_range is not None and city_name not in cities_range:
                prog.update()
                continue
            country = row[5]
            region = row[8]
            den = row[12]
            latitude = row[3]
            longitude = row[4]
            longitude = float(longitude)
            latitude = float(latitude)
            ranking = int(row[-3])

            city_entity = {
                    "city_name": city_name,
                    "country": country,
                    "region": region,
                    "density": float(den),
                    "longitude": longitude,
                    "latitude": latitude,
                    "capital": row[-7],
                    "ranking": ranking,
                }

            if country not in dict_region2cities:
                dict_region2cities[country] = {}

            if region not in dict_region2cities[country]:
                dict_region2cities[country][region] = []

            dict_region2cities[country][region].append(city_entity)
            prog.update()

    # sort every city list
    for country in dict_region2cities.keys():
        for region in dict_region2cities[country]:
            city_list = dict_region2cities[country][region]
            density_list = [c["density"] for c in city_list]
            density_local_max = max(density_list)
            for c in city_list:
                c["score"] = (5 - c["ranking"]) + c["density"] / (density_local_max + 0.0000001)
            dict_region2cities[country][region] = sorted(city_list, key=lambda x: -x["score"])

    return dict_region2cities


def build_dict_rectangle2cities(raw_data_path, gran, cities_range=None):
    '''
    :param raw_data_path:
    :param gran: granularity of division e.g. gran = 1 means divide the whole raw data into a lot of rectangle area by 1*1(lon, lat)
    :param cities_range: only consider cities in the range
    :return:
    '''
    offset_lon = 180
    offset_lat = 90
    coordinate_range_2_cities = list(np.zeros([int(360 / gran), int(180 / gran)], dtype=int).tolist())

    prog = pyprind.ProgBar(4181951 + int((360 * 180) / math.pow(gran, 2)))
    logging.warning("start building dict rectangle2cities...")
    with open(raw_data_path, 'r', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in islice(reader, 1, None):
            city_name = row[0]
            if cities_range is not None and city_name not in cities_range:
                prog.update()
                continue
            country = row[5]
            den = row[12]
            latitude = row[3]
            longitude = row[4]
            longitude = float(longitude)
            latitude = float(latitude)

            lon_map_ind = (longitude + offset_lon) / gran
            lat_map_ind = (latitude + offset_lat) / gran
            hold = coordinate_range_2_cities[int(lon_map_ind)][int(lat_map_ind)] # hold the pointer
            if isinstance(hold, int) and hold == 0: # nothing here, create a list and put this city in
                coordinate_range_2_cities[int(lon_map_ind)][int(lat_map_ind)] = [{
                    "city_name": city_name,
                    "country": country,
                    "region": row[8],
                    "density": float(den),
                    "longitude": longitude,
                    "latitude": latitude,
                    "capital": row[-7],
                    "ranking": int(row[-3]),
                }, ]
            else: # already a list here, append this new city
                coordinate_range_2_cities[int(lon_map_ind)][int(lat_map_ind)].append({
                    "city_name": city_name,
                    "country": country,
                    "region": row[8],
                    "density": float(den),
                    "longitude": longitude,
                    "latitude": latitude,
                    "capital": row[-7],
                    "ranking": int(row[-3]),
                })
            prog.update()

        for lon in range(int(360 / gran)):
            for lat in range(int(180 / gran)):
                cities = coordinate_range_2_cities[lon][lat]
                if isinstance(cities, int) and cities == 0:
                    coordinate_range_2_cities[lon][lat] = None
                else:
                    density_list = [c["density"] for c in cities]
                    density_local_max = max(density_list)
                    for c in cities:
                        c["score"] = (5 - c["ranking"]) + c["density"] / (density_local_max + 0.0000001)

                    dict_rank_2_cities = {}
                    for c in cities:
                        if c["ranking"] not in dict_rank_2_cities:
                            dict_rank_2_cities[c["ranking"]] = [c, ]
                        else:
                            dict_rank_2_cities[c["ranking"]].append(c)

                    for rank, cities_r in dict_rank_2_cities.items():
                        dict_rank_2_cities[rank] = sorted(cities_r, key=lambda x: -x["score"])

                    coordinate_range_2_cities[lon][lat] = dict_rank_2_cities

                prog.update()
    return coordinate_range_2_cities


if __name__ == "__main__":
    # cities_text = open("../city.txt", "r", encoding="utf-8").read()
    # cities = re.findall('"key": "(.*)",', cities_text)
    coordinate_range_2_cities = build_dict_region2cities("./Sources/worldcities.csv")
    json.dump(coordinate_range_2_cities, open("./Sources/dict_all_cities_region2cities.json", "w", encoding="utf-8"))
    pass
