from flask import Flask, jsonify, request, session
import mysql.connector
import bcrypt

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
    

##### METÓDO POST PARA LOGIN DO USUÁRIO (VENDEDORES) #####
    @app.route('/items/login', methods=['POST'])
    def login_usuario_vendedor():
        
        login = request.get_json()
        
        usuario = login.get('name')
        senha   = login.get('password')
        
        cursor = conexao.cursor()

        verificar_credenciais_sql = f'SELECT iduser, name, password FROM user WHERE name = "{usuario}" and type = "vendedor"'
        
        cursor.execute(verificar_credenciais_sql)
        
        resultado = cursor.fetchone()
        cursor.close()

        if resultado:
            # Verifique a senha criptografada usando bcrypt
            senha_criptografa = resultado[2].encode('utf-8')
            
            if bcrypt.checkpw(senha.encode('utf-8'), senha_criptografa):
                session['name'] = usuario

                response = {
                    'id'        : resultado[0],
                    'user'      : resultado[1],
                    'type'      : resultado[5],
                    'message'   : 'Login feito com sucesso!'
                }
                return jsonify(response)
        
        response = {
            'message': 'Dados Inválidos! Apenas Vendedores podem ter acesso.'
        }
        return jsonify(response)
########################################  


##### METÓDO POST PARA LOGOUT DO USUÁRIO (VENDEDOR) #####
    @app.route('/items/logout', methods=['POST'])
    def logout_usuario_vendedor():
        
        if 'name' in session:
        
            session.pop('name', None)

            response = {
                'user'      : session['name'],
                'message'   : 'Usuário (Vendedor) acabou de sair da sessão!'
            }
            return jsonify(response)
        
        else:
            response = {
                'message': 'Nenhum Usuário (Vendedor) logado!'
            }
            return jsonify(response)
######################################## 


##### METÓDO POST PARA CRIAR ITENS #####
    @app.route('/items', methods=['POST'])
    def criar_itens():
        
        item = request.get_json()
        
        if 'title' in item and 'author' in item and 'category_id' in item and 'price' in item and 'description' in item and 'status' in item and 'date' in item and 'saller_id' in item:
        
            titulo          = item.get('title')
            autor           = item.get('author')
            categoria_id    = item.get('category_id')
            preco           = item.get('price')
            descricao       = item.get('description')
            status          = item.get('status')
            data            = item.get('date')
            vendedor_id     = item.get('saller_id')
            
            cursor = conexao.cursor()

            criar_item_sql = f'INSERT INTO item (title, author, category_id, price, description, status, date, saller_id) VALUES ("{titulo}", "{autor}", "{categoria_id}", "{preco}", "{descricao}", "{status}", "{data}", "{vendedor_id}")' 
            cursor.execute(criar_item_sql)

            conexao.commit()
            cursor.close()

            response = {
                'message'       : 'Item criado com sucesso!',
                'title'         : titulo,
                'author'        : autor,
                'category_id'   : categoria_id,
                'price'         : preco,
                'description'   : descricao,
                'status'        : status,
                'date'          : data,
                'saller_id'     : vendedor_id
            }
            return jsonify(response)
        
        else:
            response = {
                'error': 'Verifique se os campos estão sendo inseridos corretamente!'
            }
            return jsonify(response)
########################################


##### METÓDO GET PARA LISTAR ITENS #####
    @app.route('/items', methods=['GET'])
    def mostrar_itens():
        
        if 'name' not in session:
            response = {
                'message': 'Realize o login primeiro!'
            }
            return jsonify(response)
        
        cursor = conexao.cursor()
        
        recuperar_item_sql = "SELECT * FROM item"       
        cursor.execute(recuperar_item_sql)
        
        items = cursor.fetchall()
        cursor.close()

        item_json = [
            {
                'id'            : u[0], 
                'title'         : u[1], 
                'author'        : u[2], 
                'category_id'   : u[3], 
                'price'         : u[4], 
                'description'   : u[5],
                'status'        : u[6],
                'date'          : u[7],
                'saller_id'     : u[8]
            } 
            for u in items
        ]
        return jsonify(item_json)
######################################################


##### METÓDO GET PARA LISTAR ITEM ESPECÍFICO #####
    @app.route('/items/<int:id>', methods=['GET'])
    def mostrar_item_especifico(id):
        
        if 'name' not in session:
            response = {
                'message': 'Realize o login primeiro!'
            }
            return jsonify(response)
        
        cursor = conexao.cursor()
        
        recuperar_item_sql = f'SELECT * FROM item WHERE iditem = "{id}"'       
        cursor.execute(recuperar_item_sql)
        
        items = cursor.fetchall()
        cursor.close()

        item_json = [
            {
                'id'            : u[0], 
                'title'         : u[1], 
                'author'        : u[2], 
                'category_id'   : u[3], 
                'price'         : u[4], 
                'description'   : u[5],
                'status'        : u[6],
                'date'          : u[7],
                'saller_id'     : u[8]
            } 
        ]
        return jsonify(item_json)
######################################################


##### METÓDO PUT PARA EDITAR ITENS #####
    @app.route('/items/<int:id>', methods=['PUT'])
    def editar_item(id):
        
        if 'name' not in session:
            response = {
                'message': 'Realize o login primeiro!'
            }
            return jsonify(response)
        
        editar_item = request.get_json()
        
        titulo          = item.get('title')
        autor           = item.get('author')
        categoria_id    = item.get('category_id')
        preco           = item.get('price')
        descricao       = item.get('description')
        status          = item.get('status')
        data            = item.get('date')
        vendedor_id     = item.get('saller_id')
        
        cursor = conexao.cursor()

        editar_item_sql = f'UPDATE item SET title = "{titulo}", author = "{autor}", category_id = "{categoria_id}", price = "{preco}", description = "{descricao}", status = "{status}", date = "{data}", saller_id = "{vendedor_id}" WHERE iditem = "{id}"'
        
        cursor.execute(editar_item_sql)

        conexao.commit()
        cursor.close()

        response = {
            'message'       : 'Item editado com sucesso!',
            'id'            : u[0], 
            'title'         : u[1], 
            'author'        : u[2], 
            'category_id'   : u[3], 
            'price'         : u[4], 
            'description'   : u[5],
            'status'        : u[6],
            'date'          : u[7],
            'saller_id'     : u[8]
        }
        return jsonify(response)
########################################


##### METÓDO DEL PARA DELETAR USUÁRIOS #####
    @app.route('/items/<int:id>', methods=['DELETE'])
    def excluir_item(id):
    
        if 'name' not in session:
            response = {
                'message': 'Realize o login primeiro!'
            }
            return jsonify(response)
    
        cursor = conexao.cursor()

        excluir_item_sql = f'DELETE FROM item WHERE iditem = "{id}"'  
        
        cursor.execute(excluir_item_sql)  

        conexao.commit()
        cursor.close()

        response = {
            'message': 'Item excluído com sucesso!'
        }
        return jsonify(response)
######################################## 


else:
    print("Não foi possível conectar com o MySql!!")

app.run(port=5000, host='localhost', debug=True)