from flask import Flask, jsonify, request, session
import mysql.connector
import bcrypt


app = Flask(__name__)


conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='vieira1234',
    database='seboonline',
)

if conexao.is_connected():
    print("\nConexão ao MySQL bem-sucedida!\n")


##### METÓDO POST PARA CRIAR CATEGÓRIAS #####
    @app.route('/categories', methods=['POST'])
    def criar_categoria():
        
        categoria = request.get_json()
        
        if 'name' in categoria and 'description' in categoria:
        
            nome        = categoria.get('name')
            descricao   = categoria.get('description')
            
            cursor = conexao.cursor()

            criar_categoria_sql = 'INSERT INTO category (name, description) VALUES (%s, %s)' 
            cursor.execute(criar_categoria_sql, (nome, descricao))

            conexao.commit()
            cursor.close()

            response = {
                'message'       : 'Categoria criado com sucesso!',
                'data_category' : categoria
            }
            return jsonify(response)
        
        else:
            response = {
                'error': 'Verifique se os campos estão inseridos corretamentes!'
            }
            return jsonify(response)
########################################


##### METÓDO PUT PARA EDITAR ALGUMA CATEGORIA #####
    @app.route('/categories/<int:id>', methods=['PUT'])
    def editar_categoria(id):
        
        categoria = request.get_json()
        
        if 'name' in categoria and 'description' in categoria:
        
            nome        = categoria.get('name')
            descricao   = categoria.get('description')
        
            cursor = conexao.cursor()

            editar_categoria_sql = 'UPDATE category SET name = %s, description = %s WHERE idcategory = %s' 
            cursor.execute(editar_categoria_sql, (nome, descricao, id))

            conexao.commit()
            cursor.close()

            response = {
                'message'           : 'Categoria editada com sucesso!',
                'update_category'   : categoria
            }
        
        else:
            response = {
                'error': 'Verifique se os campos estão inseridos corretamentes!'
            }
        return jsonify(response)
######################################## 


##### METÓDO GET PARA LISTAR TODAS AS CATEGORIA #####
    @app.route('/categories/', methods=['GET'])
    def mostrar_categoria():
        
        cursor = conexao.cursor()
        
        listar_categoria_sql = "SELECT * FROM category"       
        cursor.execute(listar_categoria_sql)
        
        categorias = cursor.fetchall()
        cursor.close()

        categorias_json = [
            {
                'id'            : u[0], 
                'category'      : u[1], 
                'description'   : u[2]
            } 
            
            for u in categorias
        ]
        return jsonify(categorias_json)
########################################


##### METÓDO DEL PARA DELETAR CATEGÓRIAS #####
    @app.route('/categories/<int:id>', methods=['DELETE'])
    def excluir_categoria(id):
    
        cursor = conexao.cursor()

        excluir_categoria_sql = 'DELETE FROM category WHERE idcategory = %s'  
        
        cursor.execute(excluir_categoria_sql, (id,))  

        conexao.commit()
        cursor.close()

        response = {
            'message': 'Categoria excluído com sucesso!'
        }
        return jsonify(response)
########################################


else:
    print("Não foi possível conectar com o MySql!!")

app.run(port=5000, host='localhost', debug=True)