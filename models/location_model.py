from datetime import datetime

from db.db import DB

from objects.ship import Ship
from objects.location import Location


class LocationModel:

    def __init__(self, db: DB):
        self.db = db

    def get_ship_locations(self, ship_id, dt_from: datetime, dt_to: datetime):
        sql_list = ["SELECT latitude, longitude, date_created",
                    "FROM locations",
                    f"WHERE shipid = {ship_id}"]
        if dt_from and dt_to:
            sql_list.extend([f"AND date_created >= '{dt_from}'", f"AND date_created <= '{dt_to}'"])
        res = self.db.select(" ".join(sql_list))
        if res.get('rows'):
            return [Location(latitude=x[0], longitude=x[1], dt=x[2]).to_dict() for x in res['rows']]
        raise Exception("no location logs for ship on given dates")

    def get_ships_by_location(self, location: Location):
        sql_list = ["SELECT shipid, name, type",
                    "FROM locations l",
                    "LEFT JOIN ship s",
                    "ON l.shipid = s.id",
                    f"WHERE latitude = {location.latitude}",
                    f"AND longitude = {location.longitude}",
                    "GROUP BY shipid"]
        res = self.db.select(" ".join(sql_list))
        if res.get('rows'):
            return [Ship(ship_id=x[0], name=x[1], ship_type=x[2]).to_dict() for x in res['rows']]
        raise Exception("no ships found on filtered location")
