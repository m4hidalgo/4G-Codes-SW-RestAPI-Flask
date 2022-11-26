"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Favorite_People, Favorite_Planet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

###### METODOS PARA OBTENER USUARIOS Y AÑADIRLOS ######

@app.route('/users', methods=['GET', 'POST'])
def handle_hello():

    if (request.method == 'POST'):
        body = request.get_json()
        print('POST', body)
        user = User(
            email = body['email'],
            password = body['password'],
            is_active = body['is_active']
            )
        db.session.add(user)
        db.session.commit()

        response_body = {
        "msg": "Hello, user added successfully!"
        }

        return jsonify(response_body), 200

    if (request.method == 'GET'):
        all_users = User.query.all()
        all_users = list(map(lambda x: x.serialize(), all_users))
        response_body = all_users

        return jsonify(response_body), 200

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

####### METODO PARA AÑADIR PERSONAJES Y PLANETAS #######

@app.route('/people', methods=['POST'])
def handle_people():

    if (request.method == 'POST'):
        body = request.get_json()
        character = People(
            name = body['name'],
            height = body['height'],
            mass = body['mass']
            )
        db.session.add(character)
        db.session.commit()

        response_body = {
        "msg": "Hello, character added successfully!"
        }

        return jsonify(response_body), 200

@app.route('/planets', methods=['POST'])
def handle_planets():

    if (request.method == 'POST'):
        body = request.get_json()
        planet = Planet(
            name = body['name'],
            population = body['population'],
            climate = body['climate'],
            terrain = body['terrain']
            )
        db.session.add(planet)
        db.session.commit()

        response_body = {
        "msg": "Hello, planet added successfully!"
        }

        return jsonify(response_body), 200

# METODOS PARA OBTENER PERSONAJES Y PLANETAS

@app.route('/people', methods=['GET'])
def handle_get_people():

        all_people = People.query.all()
        all_people = list(map(lambda x: x.serialize(), all_people))
        response_body = all_people

        return jsonify(response_body), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def handle_people_with_id(people_id):

        one_people = People.query.filter(People.id==people_id)
        one_people = list(map(lambda x: x.serialize(), one_people))
        response_body = one_people

        return jsonify(response_body), 200

@app.route('/planets', methods=['GET'])
def handle_get_planets():

        all_planets = Planet.query.all()
        all_planets = list(map(lambda x: x.serialize(), all_planets))
        response_body = all_planets

        return jsonify(response_body), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def handle_planet_with_id(planet_id):

        one_planet = Planet.query.filter(Planet.id==planet_id)
        one_planet = list(map(lambda x: x.serialize(), one_planet))
        response_body = one_planet

        return jsonify(response_body), 200

# METODO PARA OBTENER FAVORITOS

@app.route('/users/favorites', methods=['GET'])
def handle_list_favorites():

    if (request.method == 'GET'):
        user = 8
        all_favorites = Favorite_Planet.query.filter(Favorite_Planet.user_id==user)
        all_favorites = list(map(lambda x: x.serialize(), all_favorites))
        response_body = all_favorites

        return jsonify(response_body), 200

@app.route('/users/favorites/all', methods=['GET'])
def handle_all_favorites():

    all_favs = []

    user = 6
    all_favorites_pp = Favorite_People.query.filter(Favorite_People.user_id==user)
    all_favorites_pp = list(map(lambda x: x.serialize(), all_favorites_pp))
    all_favs.append(all_favorites_pp)

    all_favorites_pl = Favorite_Planet.query.filter(Favorite_Planet.user_id==user)
    all_favorites_pl = list(map(lambda x: x.serialize(), all_favorites_pl))
    all_favs.append(all_favorites_pl)

    response_body = all_favs

    return jsonify(response_body), 200

# METODOS PARA AÑADIR FAVORITOS

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def handle_planet_favorites(planet_id):

    if (request.method == 'POST'):
        if (planet_id > 0):
            
            favorite = Favorite_Planet(
                user_id = 6,
                planet_id = planet_id
                )
            db.session.add(favorite)
            db.session.commit()

            response_body = {
            "msg": "Hello, favorite planet added successfully!"
            }

            return jsonify(response_body), 200

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def handle_people_favorites(people_id):

    if (request.method == 'POST'):
        if (people_id > 0):
            
            favorite = Favorite_People(
                user_id = 6,
                people_id = people_id,
                )
            db.session.add(favorite)
            db.session.commit()

            response_body = {
            "msg": "Hello, favorite character added successfully!"
            }

            return jsonify(response_body), 200

# METODOS PARA BORRAR FAVORITOS

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def handle_delete_favorite_pl(planet_id):

    if (planet_id > 0):

        kwargs = {Favorite_Planet.user_id: 8, Favorite_Planet.planet_id: planet_id}
        
        db.session.query(Favorite).filter(**kwargs).delete()
        db.session.commit()

        response_body = {
            "msg": "Hello, favorite deleted successfully!",
        }

        return jsonify(response_body), 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def handle_delete_favorite_pp(people_id):

    if (people_id > 0):

        kwargs = {Favorite_People.user_id: 8, Favorite_People.people_id: people_id}
        
        db.session.query(Favorite_People).filter(**kwargs).delete()
        db.session.commit()

        response_body = {
            "msg": "Hello, favorite deleted successfully!",
        }

        return jsonify(response_body), 200

@app.route('/favorite/all', methods=['DELETE'])
def handle_delete_all():
        
    db.session.query(Favorite_People).delete()
    db.session.query(Favorite_Planet).delete()
    db.session.commit()

    response_body = {
        "msg": "Hello, all favorites deleted successfully!",
    }

    return jsonify(response_body), 200

    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
