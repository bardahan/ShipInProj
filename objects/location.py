from datetime import datetime


class Location:

    def __init__(self, latitude: float, longitude: float, dt: datetime = None):
        self.date = dt
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        try:
            assert isinstance(self.latitude, float)
            assert isinstance(self.longitude, float)
        except AssertionError:
            raise Exception("wrong latitude or longitude type")

    def to_dict(self):
        d = {"datetime": self.date,
             "lat": self.latitude,
             "lon": self.longitude}
        return d
