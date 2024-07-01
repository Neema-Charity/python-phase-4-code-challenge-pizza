#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response ,jsonify
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

@app.route("/restaurants", methods=["GET", ])
def get_restaurants():
    restaurants = []
    for restaurant in Restaurant.query.all():
        restaurant_dict = {
            "address": restaurant.address,
            "id": restaurant.id,
            "name": restaurant.name
        }
        restaurants.append(restaurant_dict)
    response = make_response(
        jsonify(restaurants),
        200
    )
    return response

@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant_id(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        restaurant_dict = {
            "address": restaurant.address,
            "id": restaurant.id,
            "name": restaurant.name
        }
        response = make_response(
            jsonify(restaurant_dict),
            200
        )
        return response
    else:
        response = make_response(
            jsonify({"error": "Restaurant not found"}),
            404
        )
        return response

@app.route('/restaurants/<int:id>', methods = ['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        db.session.delete(restaurant)
        db.session.commit()
        response = make_response(
            jsonify({"message": "Restaurant deleted"}),
            200
        )
        return response
    else:
        response = make_response(
            jsonify({"error": "Restaurant not found"}),
            404
        )
        return response

@app.route("/pizzas", methods=["GET", ])
def get_pizzas():
    pizzas = []
    for pizza in Pizza.query.all():
        pizza_dict = {
            "ingredients": pizza.ingredients,
            "id": pizza.id,
            "name": pizza.name
        }
        pizzas.append(pizza_dict)
    response = make_response(
        jsonify(pizzas),
        200
    )
    return response



@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    try:
        # Retrieve form data
        restaurant_id = request.form.get('restaurant_id')
        pizza_id = request.form.get('pizza_id')
        price = request.form.get('price')

        # Ensure all required fields are present
        if not restaurant_id or not pizza_id or not price:
            missing_fields = []
            if not restaurant_id:
                missing_fields.append('restaurant_id')
            if not pizza_id:
                missing_fields.append('pizza_id')
            if not price:
                missing_fields.append('price')
            return make_response(jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400)

        # Create new RestaurantPizza object
        new_restaurant_pizza = RestaurantPizza(
            restaurant_id=restaurant_id,
            pizza_id=pizza_id,
            price=price
        )

        db.session.add(new_restaurant_pizza)
        db.session.commit()

        # Serialize the new object
        restaurant_pizza_dict = new_restaurant_pizza.to_dict()

        # Create and return response
        response = make_response(
            jsonify(restaurant_pizza_dict), 
            201
        )
        return response
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 400)

if __name__ == "__main__":
    app.run(port=5555, debug=True)
