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


else:
    print("Não foi possível conectar com o MySql!!")

app.run(port=5000, host='localhost', debug=True)