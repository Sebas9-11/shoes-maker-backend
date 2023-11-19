from config.db import app, db, ma

class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    price = db.Column(db.Float)
    unit_payment = db.Column(db.Float)
    pay_packet = db.Column(db.Float)
    type = db.Column(db.String(45))

    def __init__(self, name, price, unit_payment, pay_packet, type):
        self.name = name
        self.price = price
        self.unit_payment = unit_payment
        self.pay_packet = pay_packet
        self.type = type

with app.app_context():
    db.create_all()

class ProductSchema(ma.Schema):
    class Meta:
        fields = ('product_id', 'name', 'price', 'unit_payment', 'pay_packet', 'type')

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
# haz las querys - ignora esto jaujaja 