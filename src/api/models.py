from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from sqlalchemy.sql import func 

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    billing = db.Column(db.String(120), nullable=False)  # Se puede cambiar a una relación si se desea
    shipping = db.Column(db.String(120), nullable=False)  # Se puede cambiar a una relación si se desea
    is_paying_customer = db.Column(db.Boolean, default=False)
    password = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "billing": self.billing,
            "shipping": self.shipping,
            "is_paying_customer": self.is_paying_customer
        }
        
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, nullable=False)  # Si necesitas relacionar a un usuario o cliente
    number = db.Column(db.String(80), nullable=False)
    order_key = db.Column(db.String(80), nullable=False)
    created_via = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(80), nullable=False)
    # date_created = db.Column(db.DateTime)
    discount_total = db.Column(db.String(80), nullable=False)
    discount_tax = db.Column(db.String(80), nullable=False)
    shipping_total = db.Column(db.String(80), nullable=False)
    total = db.Column(db.String(80), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False) 
    payment_method = db.Column(db.String(80), nullable=False)
    total_tax = db.Column(db.String(80), nullable=False)

    # customer = db.relationship('Customer', back_populates='orders')  # Relación inversa

    def __repr__(self):
        return f'<Order {self.number}>'

    def serialize(self):
        return {
            "id": self.id,
            "parent_id": self.parent_id,
            "number": self.number,
            "order_key": self.order_key,
            "created_via": self.created_via,
            "status": self.status,
            "date_created": self.date_created,
            "discount_total": self.discount_total,
            "discount_tax": self.discount_tax,
            "shipping_total": self.shipping_total,
            "total": self.total,
            "customer_id": self.customer_id,
            "payment_method": self.payment_method,
            "total_tax": self.total_tax
        }

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Identificador único
    # date_created_gmt = db.Column(db.DateTime)
    # date_modified = db.Column(db.DateTime)
    # date_modified_gmt = db.Column(db.DateTime)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    role = db.Column(db.String(120), default='customer')  # Rol por defecto
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(80), nullable=False)
    is_paying_customer = db.Column(db.Boolean, default=False)
    avatar_url = db.Column(db.String(255))  # URL para el avatar
    billing_address = db.relationship('BillingAddress', backref='customer', uselist=False)
    shipping_address = db.relationship('ShippingAddress', backref='customer', uselist=False)
    meta_data = db.relationship('MetaData', back_populates='customer', cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='customer')

    def __repr__(self):
        return f'<Customer {self.email}>'

class BillingAddress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    company = db.Column(db.String(120))
    address_1 = db.Column(db.String(255))
    address_2 = db.Column(db.String(255))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    postcode = db.Column(db.String(20))
    country = db.Column(db.String(3)) 
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))

class ShippingAddress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    company = db.Column(db.String(120))
    address_1 = db.Column(db.String(255))
    address_2 = db.Column(db.String(255))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    postcode = db.Column(db.String(20))
    country = db.Column(db.String(3)) 

class MetaData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    key = db.Column(db.String(120))
    value = db.Column(db.String(255))

    customer = db.relationship('Customer', back_populates='meta_data')