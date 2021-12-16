from flask import Flask, request, g, Response
from datetime import datetime
import json

from objects.sqlLite import SqlLite
from objects.ship import Ship
from objects.location import Location

from models.ship_model import ShipModel
from models.location_model import LocationModel

app = Flask(__name__)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/example/parameters/<int:param1>/<string:param2>', methods=['GET'])
def view_example_parameters(param1, param2):
    return {"param1": param1, "param2": param2}


@app.route('/example/posting-json', methods=['POST'])
def view_example_posting_json():
    obj = request.json
    return {"obj": obj}


# we use PUT and POST methods to store objects
@app.route('/ships', methods=['POST'])
def view_example_store_in_db():
    obj = request.json
    try:
        ship_model = ShipModel(SqlLite())
        ship = Ship(name=obj.get('name'), ship_type=obj.get('type'))
        id = ship_model.log_ship_to_db(ship)
        return {"id": id}
    except Exception as e:
        return {"err": repr(e)}


# we use GET methods to retrieve objects
@app.route('/ship/<int:id>', methods=['GET'])
def view_example_get_from_db(id):
    try:
        ship_model = ShipModel(SqlLite())
        ship = ship_model.get_ship_by_id(id)
        return {'status': 1, "id": ship.id, "name": ship.name, "type": ship.type}
    except Exception as e:
        return {'status': 0, "err": repr(e)}


@app.route('/ships/location', methods=['POST'])
def log_ship_location():
    obj = request.json
    try:
        if not (obj.get('lat') or obj.get('lon')):
            return {'status': 0, 'err': 'please detail lat and lon as flot'}
        location = Location(obj.get('lat'), obj.get('lon'))
        ship_model = ShipModel(SqlLite())
        ship_model.log_ship_location(obj.get('id'), location)
        return {'status': 1}
    except Exception as e:
        return {'status': 0, "err": repr(e)}


@app.route('/ship/<int:id>/location', methods=['GET'])
def view_ship_location(id):
    ship_id = id
    date_from = request.args.get('df')
    date_to = request.args.get('dt')
    if date_to and date_from:
        try:
            date_from = datetime.strptime(date_from, '%Y-%m-%d %H:%M:%S')
            date_to = datetime.strptime(date_to, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return {'status': 0, "err": "Please use correct date format '%Y-%m-%d %H:%M:%S'"}
    try:
        location_model = LocationModel(SqlLite())
        locations = location_model.get_ship_locations(ship_id=ship_id, dt_from=date_from, dt_to=date_to)
        return Response(response=json.dumps({'status': 1, 'id': id, 'locations': locations}), status=200,
                        mimetype="application/json")
    except Exception as e:
        return {'status': 0, "err": repr(e)}


@app.route('/location', methods=['GET'])
def view_ships_by_location():
    try:
        try:
            latitude = float(request.args.get('lat'))
            longitude = float(request.args.get('lon'))
        except ValueError:
            return {'status': 0, "err": "Please add lat & lon params as float/int"}
        location = Location(latitude=latitude, longitude=longitude)
        location_model = LocationModel(SqlLite())
        ships_dict = location_model.get_ships_by_location(location=location)
        return Response(response=json.dumps({'status': 1, 'ships': ships_dict}), status=200,
                        mimetype="application/json")
    except Exception as e:
        return {'status': 0, "err": repr(e)}


if __name__ == '__main__':
    import sys
    app.run(port=int(sys.argv[1]))
