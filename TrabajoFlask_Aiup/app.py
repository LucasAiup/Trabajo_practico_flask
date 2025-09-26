from flask import Flask, render_template, request, redirect, url_for, flash
from models.models import *
from werkzeug.security import check_password_hash
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/tpflask_aiup'
app.config['SECRET_KEY'] = 'clave_secreta'
db.init_app(app)

@app.before_request
def create_tables():
    app.before_request_funcs[None].remove(create_tables)
    db.create_all()
@app.route('/login', methods=['GET', 'POST'])

def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(nombre=username).first()
        if user and check_password_hash(user.password, password):
            flash('Login exitoso!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/CrudClientes', methods=['GET', 'POST'])
def CrudClientes():
    if request.method == 'POST':
        query_type = request.form['query_type']
        if query_type=="1":
            nombre = request.form['Nombre']
            direccion = request.form['direccion']
            telefono = request.form['telefono']
            email = request.form['email']
            new_cliente= clientes(nombre=nombre, direccion=direccion, telefono=telefono, email=email)
            db.session.add(new_cliente)
            db.session.commit()
        elif query_type=="3":
            id_cliente = request.form['id_cliente']
            cliente_to_delete = db.session.get(clientes, id_cliente)
            db.session.delete(cliente_to_delete)
            db.session.commit()
    data= db.session.query(clientes).all()
    return render_template('CrudClientes.html', data=data)

@app.route('/Editclientes', methods=['GET', 'POST'])
def EditClientes():
    if request.method == 'POST':
        id_cliente = request.form['id_cliente']
        cliente_to_edit = db.session.get(clientes, id_cliente)
    elif request.method == 'GET':
        id_cliente = request.args.get('id_cliente')
        cliente_to_edit = db.session.get(clientes, id_cliente)
        cliente_to_edit.nombre = request.args.get('Nombre')
        cliente_to_edit.direccion = request.args.get('direccion')
        cliente_to_edit.telefono = request.args.get('telefono')
        cliente_to_edit.email = request.args.get('email')
        query_type = request.args.get('query_type')
        db.session.commit()
        if query_type=="2":
            return redirect(url_for('CrudClientes'))
    return render_template('EditCliente.html', data=cliente_to_edit)

@app.route('/CrudProductos', methods=['GET', 'POST'])
def CrudProductos():
    if request.method == 'POST':
        query_type = request.form['query_type']
        if query_type=="1":
            descripcion = request.form['descripcion']
            precio = request.form['precio']
            stock = request.form['stock']
            new_producto= productos(descripcion=descripcion, precio=precio, stock=stock)
            db.session.add(new_producto)
            db.session.commit()
        elif query_type=="3":
            id_producto = request.form['id_producto']
            producto_to_delete = db.session.get(productos, id_producto)
            db.session.delete(producto_to_delete)
            db.session.commit()
    data= db.session.query(productos).all()
    return render_template('CrudProductos.html', data=data)

@app.route('/EditProducto', methods=['GET', 'POST'])
def EditProducto():
    if request.method == 'POST':
        id_producto = request.form['id_producto']
        producto_to_edit = db.session.get(productos, id_producto)
    elif request.method == 'GET':
        id_producto = request.args.get('id_producto')
        producto_to_edit = db.session.get(productos, id_producto)
        producto_to_edit.descripcion = request.args.get('descripcion')
        producto_to_edit.precio = request.args.get('precio')
        producto_to_edit.stock = request.args.get('stock')
        query_type = request.args.get('query_type')
        db.session.commit()
        if query_type=="2":
            return redirect(url_for('CrudProductos'))
    return render_template('Editproducto.html', data=producto_to_edit)

@app.route('/EmitirFactura', methods=['GET', 'POST'])
def EmitirFactura():
    data_clientes= db.session.query(clientes).all()
    data_productos= db.session.query(productos).all()
    if request.method == 'POST':
        id_producto = request.form['id_producto']
        id_cliente = request.form['id_cliente']
        cantidad = int(request.form['cantidad'])
        Fecha = datetime.now()
        producto= db.session.get(productos,id_producto)
        total= (producto.precio*cantidad)
        new_factura= facturas(id_cliente=id_cliente, fecha=Fecha, total=total)
        db.session.add(new_factura)
        db.session.commit()
        id_factura=new_factura.id_factura
        new_detalle_factura= detalle_factura(id_factura=id_factura, id_producto=id_producto,cantidad=cantidad,precio_unitario=producto.precio,subtotal=total)
        db.session.add(new_detalle_factura)
        db.session.commit()
    return render_template('EmitirFactura.html', Clientes=data_clientes,productos=data_productos)
@app.route('/ListarFacturas', methods=['GET', 'POST'])
def ListarFacturas():
    data= db.session.query(facturas).all()
    return render_template('ListarFacturas.html', data=data)
@app.route('/DetallesFactura', methods=['GET', 'POST'])
def DetallesFactura():
    data= db.session.query(detalle_factura).all()
    query_type = request.form['query_type']
    if query_type=="1":
        id_cliente = request.form['id_cliente']
        Fecha = request.form['fecha']
        query = db.session.query(facturas)
        if id_cliente:
            query = query.filter(facturas.id_cliente == id_cliente)
        if Fecha:
            query = query.filter(facturas.fecha == Fecha)
        facturas_data = query.all()
        detalle_factura_data=[]
        for row in facturas_data:
           detalle_factura_data.extend(db.session.query(detalle_factura).filter(detalle_factura.id_factura == row.id_factura).all())
        data = detalle_factura_data
    return render_template('DetallesFactura.html', data=data)
if __name__ == '__main__':
    app.run(debug=True)