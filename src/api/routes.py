"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Order
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv
from woocommerce import API
import logging

load_dotenv()
logging.basicConfig(level=logging.DEBUG)

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)
consumer_key = os.getenv('WC_CONSUMER_KEY')
consumer_secret = os.getenv('WC_CONSUMER_SECRET')
logging.debug(f"Consumer Key: {consumer_key}")
logging.debug(f"Consumer Secret: {consumer_secret}")

wcapi = API(
    url="https://imprimefotografia.es",  # Cambia por la URL de tu tienda
    consumer_key=os.getenv('WC_CONSUMER_KEY'),  # Coloca tu consumer key
    consumer_secret=os.getenv('WC_CONSUMER_SECRET'),  # Coloca tu consumer secret
    version="wc/v3"
)

@api.route("/login", methods=["POST"])   
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(email=email).first()
    
    if user is None:
        return jsonify({"msg": "No encuentro tu email"}), 401
    if email != user.email or password != user.password:
        return jsonify({"msg": "Email o usuario incorrecto"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)

@api.route("/signup", methods=["POST"])
def signup():
    body = request.get_json()
    user = User.query.filter_by(email=body["email"]).first()
    
    if user is None:
        user = User(email=body["email"], password=body["password"], is_active=False)
        db.session.add(user)
        db.session.commit()
        response_body = {
            "msg": "Usuario creado"
        }
        return jsonify(response_body), 200
    else:
        return jsonify({"msg": "Ya tenemos fichado un cliente con ese correo"}), 401

@api.route("/import_orders", methods=["GET"])
def import_orders():
    try:
        # Obtener órdenes de WooCommerce
        response = wcapi.get("orders")
        
        # Verifica si la respuesta es exitosa
        if response.status_code != 200:
            return jsonify({"msg": f"Error al importar órdenes: {response.text}"}), 401
        
        wc_orders = response.json()

        # Verifica que wc_orders sea una lista
        if not isinstance(wc_orders, list):
            return jsonify({"msg": "Error: formato de respuesta inesperado"}), 400

        for wc_order in wc_orders:
            # Verificar si la orden ya existe en la base de datos
            existing_order = Order.query.filter_by(id=wc_order["id"]).first()

            if not existing_order:
                # Crear y guardar la orden en la base de datos
                new_order = Order(
                    id=wc_order["id"],
                    parent_id=wc_order.get("parent_id", 0),
                    number=wc_order["number"],
                    order_key=wc_order["order_key"],
                    created_via=wc_order["created_via"],
                    status=wc_order["status"],
                    date_created=wc_order["date_created"],
                    discount_total=wc_order["discount_total"],
                    discount_tax=wc_order["discount_tax"],
                    shipping_total=wc_order["shipping_total"],
                    total=wc_order["total"],
                    customer_id=str(wc_order["customer_id"]),
                    payment_method=wc_order["payment_method"],
                    total_tax=wc_order["total_tax"]
                )
                db.session.add(new_order)

        db.session.commit()
        return jsonify({"msg": "Órdenes importadas correctamente"}), 200

    except Exception as e:
        return jsonify({"msg": f"Error al importar órdenes: {str(e)}"}), 500

   
@api.route("/orders", methods=["GET"])
# @jwt_required()
def get_orders():
    orders = Order.query.all()
    orders_serialized = [order.serialize() for order in orders]
    return jsonify(orders_serialized), 200
