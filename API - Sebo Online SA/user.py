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

### METÓDO POST PARA CRIAR / REGISTRAR USUÁRIOS ###
    @app.route('/users/signup', methods=['POST'])
    def criar_usuario():
        
        novo_user = request.get_json()

        if 'name' in novo_user and 'email' in novo_user and 'password' in novo_user and 'status' in novo_user and 'type' in novo_user:
            cursor = conexao.cursor()

            # Gere um hash da senha usando bcrypt
            senha_criptografa = bcrypt.hashpw(novo_user['password'].encode('utf-8'), bcrypt.gensalt())

            criar_usuario_sql = "INSERT INTO user (name, email, password, status, type) VALUES (%s, %s, %s, %s, %s)"

            cursor.execute(criar_usuario_sql, (
                novo_user['name'],
                novo_user['email'],
                senha_criptografa,  # Armazenar o hash da senha no banco de dados
                novo_user['status'],
                novo_user['type']
            ))

            conexao.commit()
            cursor.close()

            response = {
                'message': 'Usuário criado com sucesso!',
                'dados_user': novo_user
            }

            return jsonify(response)
        
        else:
            response = {
                'error': 'Verifique se os seguintes campos estão sendo inseridos: name, email, password, status, type'
            }

            return jsonify(response)
###################################################


### METÓDO POST PARA LOGIN DO USUÁRIO ###
    @app.route('/users/login', methods=['POST'])
    def login_usuario():
        
        login = request.get_json()
        
        usuario = login.get('name')
        senha = login.get('password')
        
        cursor = conexao.cursor()

        verificar_credenciais_sql = "SELECT iduser, name, password FROM user WHERE name = %s"
        
        cursor.execute(verificar_credenciais_sql, (usuario,))
        
        resultado = cursor.fetchone()
        cursor.close()

        if resultado:
            # Verifique a senha criptografada usando bcrypt
            stored_password = resultado[2].encode('utf-8')
            
            if bcrypt.checkpw(senha.encode('utf-8'), stored_password):
                session['name'] = usuario

                response = {
                    'id': resultado[0],
                    'name': resultado[1],
                    'message': 'Login Feito com Sucesso!'
                }
                return jsonify(response)
        
        response = {
            'message': 'Dados Inválidos!'
        }
        return jsonify(response)
########################################  


### METÓDO POST PARA LOGOUT DO USUÁRIO ###
    @app.route('/users/logout', methods=['POST'])
    def logout_usuario():
        if 'name' in session:
        
            session.pop('name', None)

            response = {
                'message': 'Usuário acabou de sair da sessão!'
            }
            return jsonify(response)
        
        else:
            response = {
                'message': 'Nenhum Usuário logado!'
            }
            return jsonify(response)
########################################


### METÓDO PUT PARA EDITAR USUÁRIOS ###
    @app.route('/users/<int:id>', methods=['PUT'])
    def editar_usuario(id):
        
        if 'name' not in session:
            response = {
                'message': 'Realize o Login primeiro!'
            }
            return jsonify(response)
        
        editar_user = request.get_json()
        
        cursor = conexao.cursor()

        editar_usuario_sql = "UPDATE user SET name = %s, email = %s, password = %s, status = %s, type = %s WHERE iduser = %s"
        
        # Hash da senha com bcrypt
        senha_criptografa = bcrypt.hashpw(editar_user['password'].encode('utf-8'), bcrypt.gensalt())
        
        cursor.execute(editar_usuario_sql, (
            editar_user['name'], 
            editar_user['email'], 
            senha_criptografa,  # Armazene a senha criptografada no banco de dados
            editar_user['status'], 
            editar_user['type'], 
            id
        ))

        conexao.commit()
        cursor.close()

        response = {
            'message': 'Usuário editado com sucesso!',
            'update_user': editar_user
        }
        return jsonify(response)
########################################


### METÓDO DEL PARA DELETAR USUÁRIOS ###
    @app.route('/users/<int:id>', methods=['DELETE'])
    def excluir_usuario(id):
    
        if 'name' not in session:
            response = {
                'message': 'Realize o Login primeiro!'
            }
            return jsonify(response)
    
        cursor = conexao.cursor()

        excluir_usuario_sql = "DELETE FROM user WHERE iduser = %s"  
        
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