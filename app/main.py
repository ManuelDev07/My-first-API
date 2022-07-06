from flask import  Flask, request, jsonify 
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

#flask-sqlaclchemy: esto permite conectarme a BBDD SQL.
#flask-marshmallow: para poder realizar esquemas de mi BBDD

#Pasos:
#Primero se debe hacer la conexión a la BBDD
#Luego crear la clase para una tabla de la BBDD
#Y por último un esquema

app = Flask(__name__)
#conexión a BBDD: (esto está en la documentación de sqlalchemy)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456789@localhost:3306/proyectopythonapi' #Conexión a la BBDD 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #Para que no salgan errores

#instancio sqlalchemy y marshmallow:
db = SQLAlchemy(app)
ma = Marshmallow(app)

#crear una clase para crear así modelar una tabla en la BBDD:
class Categoria(db.Model):
    #campos:
    cat_id = db.Column(db.Integer, primary_key=True)
    cat_nom = db.Column(db.String(120))
    cat_desc = db.Column(db.String(120))

    def __init__(self, cat_nom, cat_desc):
        self.cat_nom = cat_nom
        self.cat_desc = cat_desc

#Crear la tabla:
db.create_all()

#Creo un ESQUEMA de mi tabla para así sea más facil llamarlo cuando se necesite:
class CategoriaSchema(ma.Schema):
    #Declaro los campos que necesito: (los de la tabla)
    class Meta:
        fields = ('cat_id','cat_nom','cat_desc')

#E inicializo mi esquema(Debo hacerlo siempre antes de empezar a trabajar con mis endpoints)
#Para cuando sea una sola respuesta:
categoria_schema = CategoriaSchema()

#Para varias respuestas.
categorias_schema = CategoriaSchema(many=True)


#Mis endpoints:
@app.route('/')
def index():
    return jsonify({'message':'Welcome! to my API REST Python :D'})

#GET:
@app.route('/categoria', methods=['GET'])
def get_categorias():
    all_categorias = Categoria.query.all() #esto es para que me traiga todo
    result = categorias_schema.dump(all_categorias)

    return jsonify(result)

#GET por id:
@app.route('/categoria/<cat_id>')
def get_categoria_id(cat_id):
    just_one = Categoria.query.get(cat_id)#Será solo para obtener un id
    
    return categoria_schema.jsonify(just_one) #regreso el que fué pedido

#POST:
@app.route('/crear_categoria', methods=['POST'])
def crear_categoria():
    #Recibo los datos para rellenar los campos de la BBDD:
    #Se reciben mediante un doc JSON (el id es auto increment)
    cat_nom = request.json['cat_nom'] 
    cat_desc = request.json['cat_desc']

    #Guardo la info recibida en una variable del objeto de la clase Categoria para luego agregarla
    registrar = Categoria(cat_nom, cat_desc)

    db.session.add(registrar) #Agrego los datos a la BBDD
    db.session.commit() #Guardo los cambios

    return categoria_schema.jsonify(registrar)

#PUT:
@app.route('/edit_categoria/<cat_id>', methods=['PUT'])
def update_categoria(cat_id):
    #Consulto a la BBDD por el id del elemento
    edit_element = Categoria.query.get(cat_id)

    #capturo los datos en una variable
    cat_nom = request.json['cat_nom']
    cat_desc = request.json['cat_desc']

    edit_element.cat_nom = cat_nom
    edit_element.cat_desc = cat_desc

    db.session.commit()

    return categoria_schema.jsonify(edit_element)    

#DELETE:
@app.route('/delete_categoria/<cat_id>', methods=['DELETE'])
def delete_categoria(cat_id):
    #Capturo el elemento a eliminar mediante su id
    del_element = Categoria.query.get(cat_id)

    #elimino los datos de mi BBDD
    db.session.delete(del_element)
    db.session.commit()#Guardo los cambios

    return categoria_schema.jsonify(del_element)

if __name__ == '__main__':
    app.run(debug=True)