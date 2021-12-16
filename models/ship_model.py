from db.db import DB

from objects.ship import Ship
from objects.location import Location


class ShipModel:
    def __init__(self, db: DB):
        self.db = db

    def get_ship_by_id(self, ship_id):
        res = self.db.select("SELECT id, name, type from ship WHERE id = ?", (ship_id,))
        if res.get('rows'):
            return Ship(ship_id=res.get('rows')[0][0],
                        name=res.get('rows')[0][1],
                        ship_type=res.get('rows')[0][2])
        raise Exception("Ship not exist")

    def log_ship_to_db(self, ship: Ship):
        self.db.insert("INSERT INTO ship(name, type) values(?, ?)", (ship.name, ship.type))
        res = self.db.select("SELECT last_insert_rowid()")
        if res.get('rows'):
            return res.get('rows')[0][0]
        raise Exception("no 'id' back might be an insert issue")

    def log_ship_location(self, ship_id: int, location: Location):
        try:
            self.db.insert("INSERT INTO locations(shipid, latitude, longitude) values(?, ?, ?)", (ship_id,
                                                                                                  location.latitude,
                                                                                                  location.longitude))
        except Exception as e:
            if "IntegrityError" in repr(e):
                raise Exception(f"ship id: {ship_id} dose not exist in DB please insert it first")
            else:
                raise e
