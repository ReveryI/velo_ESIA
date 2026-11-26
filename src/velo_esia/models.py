""" Objets métier (Station, StationStatus, Snapshot, Period, etc.) """

class RequestError(Exception):
    pass

class Station:
    station_id: str
    num_bikes_available: int
    vehicle_types_available: list[dict[int, str]] # [{ count: 31, vehicle_type_id: "bike" }]
    num_docks_available: int
    is_installed: bool
    is_renting: bool
    is_returning: bool
    last_reported: int
    
    def __init__(self, station: dict):
        self.station_id = station.get("station_id", "")
        self.num_bikes_available = station.get("num_bikes_available", 0)
        self.vehicle_types_available = station.get("vehicle_types_available", [{"count": 0, "vehicle_type_id": ""}])
        self.num_docks_available = station.get("num_docks_available", 0)
        self.is_installed = station.get("is_installed", False)
        self.is_renting = station.get("is_renting", True) # ou False ?
        self.is_returning = station.get("is_returning", False) # ou True ?
        self.last_reported = station.get("last_reported", 0)
        self.station_name = self.get_station_name()

    def __repr__(self):
        return f"Station(\
station_id={self.station_id!r}, num_bikes_available={self.num_bikes_available}, \
vehicle_types_available={self.vehicle_types_available}, num_docks_available={self.num_docks_available} \
is_installed={self.is_installed}, is_renting={self.is_renting}, is_returning={self.is_returning} \
last_reported={self.last_reported}\
)"

    def from_request(request):
        if request.status_code == 200:
            raw = request.json()
            ttl = raw["ttl"]
            version = raw["version"]
            data = raw["data"]
            for station in data["stations"]:
                stations.append(Station(station=station))
        else:
            raise RequestError(r.text)
        
        return stations
    
    def get_station_name(self):
        r = requests.get("https://media.ilevia.fr/opendata/station_information.json")
        if requests.status_code == 200:
            for station in r.json()["data"]["stations"]:
                if station.get("station_id", "0") == self.station_id:
                    self.station_name = station.get("station_name", "")
            else:
                self.station_name = ""
        else:
            raise RequestError(r.text)

{'data': {'folder': '/velo_ESIA/'}, 'refresh': {'max_age_days': 7}, 'collect': {'interval_seconds': 120}, 'alerts': {'low_bikes': 2, 'low_docks': 2}, 'dashboard': {'refresh_seconds': 60}, 'logging': None, 'level': 'INFO', 'file': '/velo_ESIA/velo.log'}

class Config:
    network: dict[str, str]
    data: dict[str, str]
    
    def __init__(self, config: dict):
        self.network: dict = config.get("network", {})
        self.data: dict = config.get("data", {})
        self.refresh: dict = config.get("refresh")
        collect: dict = config.get("collect")
        
        network_name = self.network.get("name", "")
        network_gbfs_url = self.network.get("gbfs_url", "")
    

import requests

r = requests.get("https://media.ilevia.fr/opendata/station_status.json")

data = {}
stations = []
ttl = 0
version = "2.3"

if r.status_code == 200:
    raw = r.json()
    ttl = raw["ttl"]
    version = raw["version"]
    data = raw["data"]
    for station in data["stations"]:
        stations.append(Station(station=station))
else:
  print(r.text)
  
for s in stations:
    print(s)