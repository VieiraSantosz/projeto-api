from flask import Flask, jsonify, request, session
from bcrypt import gensalt, hashpw

app = Flask(__name__)
app.secret_key = 'chave_secreta'


conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='vieira1234',
    database='seboonline',
)

if conexao.is_connected():
    print("\nConexão ao MySQL bem-sucedida!\n")


### METÓDO POST PARA CRIAR CATEGÓRIAS ###
@app.route('/categories', methods=['POST'])
def criar_categoria():
    
        categoria = request.get_json()
        
        if 'name' in categoria and 'description' in categoria:
        
            nome        = categoria.get('name')
            descricao   = categoria.get('description')
            
            cursor = conexao.cursor()

            criar_categoria = f'INSERT INTO category (name, description) VALUES ("{nome}", "{descricao}")' 
            cursor.execute(criar_categoria)

            conexao.commit()
            cursor.close()

               response = {
                'message': 'Categoria criado com sucesso!',
                'dados_user': categoria
            }

            return jsonify(response)
        
        else:
            response = {
                'error': 'Verifique se os seguintes campos estão sendo inseridos: name, description'
            }

            return jsonify(response)
########################################  


### METÓDO PUT PARA EDITAR ALGUMA CATEGORIA ###
@app.route('/categories/<int:id>', methods=['PUT'])
def editar_categoria(id):
    
        editar_categoria = request.get_json()
        
        if 'name' in categoria and 'description' in categoria:
        
        nome        = categoria.get('name')
        descricao   = categoria.get('description')
        
        cursor = conexao.cursor()

        editar_categoria = f'UPDATE category SET name = "{nome}, description = "{descricao}"' 
        cursor.execute(editar_categoria)

        conexao.commit()
        cursor.close()

            response = {
            'message': 'Categoria editada com sucesso!',
            'dados_user': categoria
        }
        
        else:
            response = {
                'error': 'Verifique se os seguintes campos estão sendo inseridos: name, description'
            }

            return jsonify(response)
########################################


### METÓDO GET PARA LISTAR TODAS AS CATEGORIA ###
@app.route('/categories/', methods=['GET'])
def mostrar_categoria():
    
        cursor = conexao.cursor()
        
        listar_categoria = "SELECT * FROM user"       
        cursor.execute(listar_categoria)
        
        categorias = cursor.fetchall()
        cursor.close()

        categorias_json = [
            {
                'id'        : u[0], 
                'name'      : u[1], 
                'email'     : u[2], 
                'password'  : u[3], 
                'status'    : u[4], 
                'type'      : u[5]
            } 
            
            for u in categorias
        ]
        
        return jsonify(categorias_json)
########################################


### METÓDO DEL PARA DELETAR CATEGÓRIAS ###
    @app.route('/categories/<int:id>', methods=['DELETE'])
    def excluir_categoria(id):
    
        cursor = conexao.cursor()

        excluir_usuario_sql = "DELETE FROM category WHERE idcategory = %s"  
        
        cursor.execute(excluir_usuario_sql, (id,))  

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