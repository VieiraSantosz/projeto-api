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
    

########## PÁGINA USERS ##########
    
##### METÓDO POST PARA LOGIN DO USUÁRIO #####
    @app.route('/users/login', methods=['POST'])
    def login_usuario():
        
        login = request.get_json()
        
        usuario = login.get('name')
        senha   = login.get('password')
        
        cursor = conexao.cursor()

        verificar_credenciais_sql = 'SELECT iduser, name, password FROM user WHERE name = %s'
        
        cursor.execute(verificar_credenciais_sql, (usuario,))
        
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
                    'message'   : 'Login feito com sucesso!'
                }
                return jsonify(response)
        
        response = {
            'message': 'Dados Inválidos!'
        }
        return jsonify(response)
######################################## 


##### METÓDO POST PARA LOGOUT DO USUÁRIO #####
    @app.route('/users/logout', methods=['POST'])
    def logout_usuario():
        
        name = session.get('name')
        
        if 'name' in session:
        
            session.pop('name', None)

            response = {
                'user'      : name,
                'message'   : 'Usuário acabou de sair da sessão!'
            }
            return jsonify(response)
        
        else:
            response = {
                'message': 'Nenhum Usuário logado!'
            }
            return jsonify(response)
########################################


##### METÓDO POST PARA CRIAR / REGISTRAR USUÁRIOS #####
    @app.route('/users/signup', methods=['POST'])
    def criar_usuario():
        
        criar_user = request.get_json()

        if 'name' in criar_user and 'email' in criar_user and 'password' in criar_user and 'status' in criar_user and 'type' in criar_user:
            
            nome    = criar_user.get('name')
            senha   = criar_user.get('password')
            email   = criar_user.get('email')
            status  = criar_user.get('status')
            tipo    = criar_user.get('type')
            
            cursor = conexao.cursor()

            # Gere um hash da senha usando bcrypt
            senha_criptografada = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

            criar_usuario_sql = 'INSERT INTO user (name, email, password, status, type) VALUES (%s, %s, %s, %s, %s)'

            # Fornecendo os valores separadamente no método execute
            cursor.execute(criar_usuario_sql, (
                nome,
                email,
                senha_criptografada,
                status,
                tipo
            ))

            conexao.commit()
            cursor.close()

            response = {
                'message'   : 'Usuário criado com sucesso!',
                'data_user' : criar_user 
            }
            return jsonify(response)
        
        else:
            response = {
                'error': 'Verifique se os campos estão inseridos corretamentes!'
            }
            return jsonify(response)
###################################################


##### METÓDO PUT PARA EDITAR USUÁRIOS #####
    @app.route('/users/<int:id>', methods=['PUT'])
    def editar_usuario(id):
        
        if 'name' not in session:
            response = {
                'message': 'Realize o login primeiro!'
            }
            return jsonify(response)
        
        editar_user = request.get_json()
        
        nome    = editar_user.get('name')
        senha   = editar_user.get('password')
        email   = editar_user.get('email')
        status  = editar_user.get('status')
        tipo    = editar_user.get('type')
        
        cursor = conexao.cursor()
        
        # Hash da senha com bcrypt
        senha_criptografada = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
        
        editar_usuario_sql = 'UPDATE user SET name = %s, email = %s, password = %s, status = %s, type = %s WHERE iduser = %s'
        
        cursor.execute(editar_usuario_sql, (
                nome,
                email,
                senha_criptografada,
                status,
                tipo,
                id
            ))

        conexao.commit()
        cursor.close()

        response = {
            'message'       : 'Usuário editado com sucesso!',
            'update_user'   : editar_user
            }
        return jsonify(response)
########################################


##### METÓDO DEL PARA DELETAR USUÁRIOS #####
    @app.route('/users/<int:id>', methods=['DELETE'])
    def excluir_usuario(id):
    
        if 'name' not in session:
            response = {
                'message': 'Realize o login primeiro!'
            }
            return jsonify(response)
    
        cursor = conexao.cursor()

        excluir_usuario_sql = 'DELETE FROM user WHERE iduser = %s'  
        
        cursor.execute(excluir_usuario_sql, (id,))  

        conexao.commit()
        cursor.close()

        response = {
            'message': 'Usuário excluído com sucesso!'
        }
        return jsonify(response)
########################################

########## FIM DA PÁGINA USERS ##########


########## PÁGINA ADMINS ##########

##### METÓDO POST PARA LOGIN DE ADMINISTRADOR #####
    @app.route('/admin/login', methods=['POST'])
    def login_admin():
        
        login = request.get_json()
        
        administrador   = login.get('name')
        senha           = login.get('password')
        
        cursor = conexao.cursor()

        verificar_credenciais_sql = 'SELECT idadmin, name FROM admin WHERE name = %s AND password = %s'
        
        cursor.execute(verificar_credenciais_sql, (administrador, senha))
        
        resultado = cursor.fetchone()
        cursor.close()

        if resultado:
            
            session['name'] = administrador

            response = {
                'id'        : resultado[0],
                'admin'     : resultado[1],
                'message'   : 'Login feito com sucesso!'
            }
            return jsonify(response)
        
        else:
            response = {
                'message': 'Dados Inválidos!'
            }
            return jsonify(response)
########################################  


##### METÓDO POST PARA LOGOUT DO ADMNISTRADOR #####
    @app.route('/admin/logout', methods=['POST'])
    def logout_admin():
        
        nome = session.get('name')
        
        if 'name' in session:
            session.pop('name', None)

            response = {
                'admin'     : nome,
                'message'   : 'Administrador acabou de sair da sessão!'
            }
            return jsonify(response)
        
        else:
            response = {
                'message': 'Nenhum Administrador logado!'
            }
            return jsonify(response)
######################################## 


##### METÓDO GET PARA LISTAR USUÁRIOS #####
    @app.route('/admin/users', methods=['GET'])
    def mostrar_usuario():
        
        if 'name' not in session:
            response = {
                'message': 'Realize o login primeiro!'
            }
            return jsonify(response)
        
        cursor = conexao.cursor()
        
        listar_usuarios_sql = "SELECT * FROM user"    
           
        cursor.execute(listar_usuarios_sql)
        
        usuarios = cursor.fetchall()
        cursor.close()

        usuarios_json = [
            {
                'id'        : u[0], 
                'user'      : u[1], 
                'email'     : u[2], 
                'password'  : u[3], 
                'status'    : u[4], 
                'type'      : u[5]
            } 
            for u in usuarios
        ]
        return jsonify(usuarios_json)
########################################

########## FIM DA PÁGINA ADMINS ##########


########## PÁGINA CATEGORIES ##########

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

########## FIM DA PÁGINA CATEGORIES ##########

    
########## PÁGINA ITENS ##########

##### METÓDO POST PARA LOGIN DO USUÁRIO (VENDEDORES) #####
    @app.route('/items/login', methods=['POST'])
    def login_usuario_vendedor():
        
        login = request.get_json()
        
        usuario = login.get('name')
        senha   = login.get('password')
        
        cursor = conexao.cursor()

        verificar_credenciais_sql = 'SELECT iduser, name, password, type FROM user WHERE name = %s and type = "vendedor"'
        
        cursor.execute(verificar_credenciais_sql, (usuario,))
        
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
                    'type'      : resultado[3],
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
        
        nome = session.get('name')
        
        if 'name' in session:
        
            session.pop('name', None)

            response = {
                'user'      : nome,
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
        
        if 'name' not in session:
            response = {
                'message': 'Realize o login primeiro!'
            }
            return jsonify(response)
        
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

            criar_item_sql = 'INSERT INTO item (title, author, category_id, price, description, status, date, saller_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)' 
            cursor.execute(criar_item_sql, (
                titulo,
                autor,
                categoria_id,
                preco,
                descricao,
                status,
                data,
                vendedor_id
            ))

            conexao.commit()
            cursor.close()

            response = {
                'message'   : 'Item criado com sucesso!',
                'data_item' : item
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
        
        recuperar_item_sql = 'SELECT * FROM item WHERE iditem = %s'       
        cursor.execute(recuperar_item_sql, (id,))
        
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


##### METÓDO GET PARA LISTAR ITEM COM FILTRO (TITLE) #####
    @app.route('/items/<string:title>', methods=['GET'])
    def mostrar_item_title(title):
        
        if 'name' not in session:
            response = {
                'message': 'Realize o login primeiro!'
            }
            return jsonify(response)
        
        cursor = conexao.cursor()
        
        recuperar_item_sql = 'SELECT * FROM item WHERE title LIKE %s'       
        cursor.execute(recuperar_item_sql, ('%' + title + '%',))
        
        items = cursor.fetchall()
        cursor.close()

        if not items:
            response = {
                'message': 'Nenhum item encontrado com o título fornecido.'
            }
            return jsonify(response)

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


##### METÓDO PUT PARA EDITAR ITENS #####
    @app.route('/items/<int:id>', methods=['PUT'])
    def editar_item(id):
        
        if 'name' not in session:
            response = {
                'message': 'Realize o login primeiro!'
            }
            return jsonify(response)
        
        item = request.get_json()
        
        titulo          = item.get('title')
        autor           = item.get('author')
        categoria_id    = item.get('category_id')
        preco           = item.get('price')
        descricao       = item.get('description')
        status          = item.get('status')
        data            = item.get('date')
        vendedor_id     = item.get('saller_id')
        
        cursor = conexao.cursor()

        editar_item_sql = 'UPDATE item SET title = %s, author = %s, category_id = %s, price = %s, description = %s, status = %s, date = %s, saller_id = %s WHERE iditem = %s'
        
        cursor.execute(editar_item_sql, (
                titulo,
                autor,
                categoria_id,
                preco,
                descricao,
                status,
                data,
                vendedor_id,
                id
            ))

        conexao.commit()
        cursor.close()

        response = {
            'message'       : 'Item editado com sucesso!',
            'update_item'   : item
        }
        return jsonify(response)
########################################


##### METÓDO DEL PARA DELETAR ITEM #####
    @app.route('/items/<int:id>', methods=['DELETE'])
    def excluir_item(id):
    
        if 'name' not in session:
            response = {
                'message': 'Realize o login primeiro!'
            }
            return jsonify(response)
    
        cursor = conexao.cursor()

        excluir_item_sql = 'DELETE FROM item WHERE iditem = %s'  
        
        cursor.execute(excluir_item_sql, (id,))  

        conexao.commit()
        cursor.close()

        response = {
            'message': 'Item excluído com sucesso!'
        }
        return jsonify(response)
######################################## 

########## FIM DA PÁGINA ITENS ##########


########## PÁGINA TRANSACTIONS ##########

##### METÓDO POST PARA REGISTRAR TRANSAÇÕES #####
    @app.route('/transactions', methods=['POST'])
    def criar_transacao():
        
        transacao = request.get_json()
        
        if 'buyer_id' in transacao and 'saller_id' in transacao and 'item_id' in transacao and 'date' in transacao and 'price' in transacao:
        
            comprador_id    = transacao.get('buyer_id')
            vendedor_id     = transacao.get('saller_id')
            item_id         = transacao.get('item_id')
            data            = transacao.get('date')
            preco           = transacao.get('price')
            
            cursor = conexao.cursor()

            criar_transacao = f'INSERT INTO transaction (buyer_id, saller_id, item_id, date, price) VALUES (%s, %s, %s, %s, %s)' 
            cursor.execute(criar_transacao, (
                comprador_id,
                vendedor_id,
                item_id,
                data,
                preco
                ))

            conexao.commit()
            cursor.close()

            response = {
                'message'   : 'Transação criado com sucesso!',
                'data_transaction'  : transacao
            }
            return jsonify(response)
        
        else:
            response = {
                'error': 'Verifique se os campos estão sendo inseridos corretamente!'
            }
            return jsonify(response)
########################################


##### METÓDO GET PARA LISTAR UMA TRANSAÇÃO ESPECÍFICA #####
    @app.route('/transactions/<int:id>', methods=['GET'])
    def mostrar_transacao_especifico(id):
            
            cursor = conexao.cursor()
            
            recuperar_transacao_sql = 'SELECT idtransaction, buyer_id, buyer_name, saller_id, saller_name, item_id, item_name, date, price FROM users_transaction WHERE saller_id = %s'       
            cursor.execute(recuperar_transacao_sql, (id,))
            
            transacao = cursor.fetchall()
            cursor.close()

            transacao_json = [
                {
                    'idtransaction' : u[0], 
                    'buyer_id'      : u[1],
                    'buyer_name'    : u[2],
                    'saller_id'     : u[3],
                    'saller_name'   : u[4], 
                    'item_id'       : u[5],
                    'item_name'     : u[6], 
                    'date'          : u[7], 
                    'price'         : u[8]
                } 
                for u in transacao
            ]
            return jsonify(transacao_json)
######################################################

########## FIM DA PÁGINA TRANSACTIONS ##########

else:
    print("Não foi possível conectar com o MySql!!")

app.run(port=5000, host='localhost', debug=True)
