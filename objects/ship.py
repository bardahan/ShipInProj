class Ship:

    def __init__(self, ship_id: int = None, name: str = None, ship_type: str = None,):
        self.id = ship_id
        self.name = name
        self.type = ship_type

    def __str__(self):
        string_list = []
        if self.id:
            string_list.append(f"date: {self.id}")
        if self.name:
            string_list.append(f"latitude: {self.name}")
        if self.type:
            string_list.append(f"longitude: {self.type}")
        return ", ".format(string_list)

    def to_dict(self):
        d = {}
        if self.id:
            d['id'] = self.id
        if self.name:
            d['name'] = self.name
        if self.type:
            d['type'] = self.type
        return d
