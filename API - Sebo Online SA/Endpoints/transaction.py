from flask import Flask, jsonify, request, session
import mysql.connector
import bcrypt

app = Flask(__name__)


conexao = mysql.connector.connect (
    host     = 'host',
    user     = 'user',
    password = 'password',
    database = 'database',
)

if conexao.is_connected():
    print("\nConexão ao MySQL bem-sucedida!\n")


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


else:
    print("Não foi possível conectar com o MySql!!")

app.run(port=5000, host='localhost', debug=True)
