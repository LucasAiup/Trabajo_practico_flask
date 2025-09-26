from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

db = SQLAlchemy()
class detalle_factura(db.Model):
    __tablename__ = 'detalle_factura'
    id_detalle = db.Column(db.Integer, primary_key=True)
    id_factura = db.Column(db.Integer, db.ForeignKey("facturas.id_factura"))
    id_producto = db.Column(db.Integer, db.ForeignKey("productos.id_producto"))
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return f'<User {self.id_detalle}>'

class User(db.Model):
    __tablename__ = 'usuarios'
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True,nullable=False)
    email = db.Column(db.String(50), unique=True,nullable=False)
    password = db.Column(db.String(100), nullable=False)
    rol = db.Column(db.String(50), unique=False,nullable=False)
    def __repr__(self):
        return f'<User {self.nombre}>'

class productos(db.Model):
    __tablename__ = 'productos'
    id_producto = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(500), nullable=False)
    precio = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    detalle_factura = db.relationship('detalle_factura',backref='producto',lazy=True)
    def __repr__(self):
        return f'<User {self.id_producto}>'

class clientes(db.Model):
    __tablename__ = 'clientes'
    id_cliente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    direccion = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True,nullable=False)
    facturas = db.relationship('facturas',backref='cliente',lazy=True)
    def __repr__(self):
        return f'{self.id_cliente} {self.nombre} {self.direccion} {self.telefono} {self.email}'

class facturas(db.Model):
    __tablename__ = 'facturas'
    id_factura = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey("clientes.id_cliente"))
    fecha = db.Column(db.Date, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    detalle_factura = db.relationship('detalle_factura',backref='factura',lazy=True)
    def __repr__(self):
        return f'<User {self.id_factura}>'