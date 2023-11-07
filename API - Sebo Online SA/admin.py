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


##### METÓDO POST PARA LOGIN DE ADMINISTRADOR #####
    @app.route('/admin/login', methods=['POST'])
    def login_admin():
        
        login = request.get_json()
        
        administrador   = login.get('name')
        senha           = login.get('password')
        
        cursor = conexao.cursor()

        verificar_credenciais_sql = f'SELECT idadmin, name FROM admin WHERE name = "{administrador}" AND password = "{senha}"'
        
        cursor.execute(verificar_credenciais_sql)
        
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
        
        if 'name' in session:
            session.pop('name', None)

            response = {
                'admin'     : session['name'],
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


else:
    print("Não foi possível conectar com o MySql!!")

app.run(port=5000, host='localhost', debug=True)