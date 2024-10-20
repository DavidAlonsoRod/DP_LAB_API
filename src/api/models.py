from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(120), unique=True, nullable=False)
    last_name = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    billing = db.Column(db.String(120), unique=True, nullable=False)
    shipping = db.Column(db.String(120), unique=True, nullable=False)
    is_paying_customer = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

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
            # do not serialize the password, its a security breach
        }
        
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, unique=False, nullable=False)
    number = db.Column(db.String(80), unique=False, nullable=False)
    order_key = db.Column(db.String(80), unique=False, nullable=False)
    created_via = db.Column(db.String(80), unique=False, nullable=False)
    status = db.Column(db.String(80), unique=False, nullable=False)
    date_created = db.Column(db.String(80), unique=False, nullable=False)
    discount_total = db.Column(db.String(80), unique=False, nullable=False)
    discount_tax = db.Column(db.String(80), unique=False, nullable=False)
    shipping_total = db.Column(db.String(80), unique=False, nullable=False)
    total = db.Column(db.String(80), unique=False, nullable=False)
    customer_id = db.Column(db.String(80), unique=False, nullable=False)
    payment_method = db.Column(db.String(80), unique=False, nullable=False)
    total_tax = db.Column(db.String(80), unique=False, nullable=False)
    
    
   
    def __repr__(self):
        return f'<Order {self.order}>'

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
            "total_tax": self.total_tax,
            # do not serialize the password, its a security breach
        }



