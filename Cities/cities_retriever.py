from Cities import settings
import json
import time
import logging


class CitiesRetriever:
    def __init__(self, dict_file_path):
        self.gran = settings.GRANULARITY
        try:
            logging.warning("Try to load the city dict...")
            t1 = time.time()
            self.dict = json.load(open(dict_file_path, "r", encoding="utf-8"))
            t2 = time.time()
            logging.warning("done in %f s." % (t2 - t1))
        except:
            logging.warning("No dict file founded, please check the path...")
        pass

    def in_rectangle(self, city, lon_start, lon_end, lat_start, lat_end):
        city_lon = city["longitude"]
        city_lat = city["latitude"]
        # check longitude
        if lon_start < lon_end:
            if city_lon < lon_start or city_lon > lon_end:
                return False
        else:
            if lon_end < city_lon < lon_start:
                return False

        # check latitude
        if lat_start < lat_end:
            if city_lat < lat_start or city_lat > lat_end:
                return False
        else:
            if lat_end < city_lat < lat_start:
                return False
        return True

    def retrieve_cities(self, lon_start, lon_end, lat_start, lat_end, num):
        offset_lon = 180
        offset_lat = 90
        gran = self.gran
        dict = self.dict

        lon_start_ind = int((lon_start + offset_lon) / gran)
        lat_start_ind = int((lat_start + offset_lat) / gran)
        lon_end_ind = int((lon_end + offset_lon) / gran)
        lat_end_ind = int((lat_end + offset_lat) / gran)

        t1 = time.time()
        rank_2_candidates = {"1": [], "2": [], "3": [], "4": [], "5": []}
        slice_lon = None
        if lon_start_ind <= lon_end_ind:
            slice_lon = dict[lon_start_ind: lon_end_ind + 1]
        else:
            slice_lon = dict[:lon_end_ind + 1] + dict[lon_start_ind:]

        if lat_start_ind <= lat_end_ind:
            for slice in slice_lon:
                for cluster in slice[lat_start_ind:lat_end_ind + 1]:
                    if cluster is None:
                        continue
                    for rank, cities in cluster.items():
                        if rank in rank_2_candidates:
                            rank_2_candidates[rank].extend(cities)
                        else:
                            rank_2_candidates[rank] = list(cities)
        else:
            for slice in slice_lon:
                for cluster in (slice[:lat_end_ind + 1] + slice[lat_start_ind:]):
                    if cluster is None:
                        continue
                    for rank, cities in cluster.items():
                        if rank in rank_2_candidates:
                            rank_2_candidates[rank].extend(cities)
                        else:
                            rank_2_candidates[rank] = list(cities)

        t2 = time.time()
        candidates = []
        for rank, cities in rank_2_candidates.items():
            for c in cities:
                if not self.in_rectangle(c, lon_start, lon_end, lat_start, lat_end):
                    continue
                candidates.append(c)
                if len(candidates) >= num:
                    break
            if len(candidates) >= num:
                break

        winners = sorted(candidates, key=lambda x: -x["score"])
        if len(winners) > num:
            winners = winners[:num]
        t3 = time.time()
        # print("t2 - t1: %f, t3 - t2: %f" % (t2 - t1, t3 - t2))
        return winners


if __name__ == "__main__":
    cr = CitiesRetriever("Sources/dict_1.json")
    cities = cr.retrieve_cities(-124.71, -77.21, 25.24, 44.75, 500000)
    print(len(cities))
    # print(json.dumps(cities, indent=2))
