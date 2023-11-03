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


### METÓDO POST PARA REGISTRAR TRANSAÇÕES ###
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

                criar_transacao = f'INSERT INTO transaction (buyer_id, saller_id, item_id, date, price) VALUES ("{comprador_id}", "{vendedor_id}", "{item_id}", "{data}", "{preco}")' 
                cursor.execute(criar_transacao)

                conexao.commit()
                cursor.close()

                response = {
                    'message'   : 'Transção criado com sucesso!',
                    'buyer_id'  : comprador_id,
                    'saller_id' : vendedor_id,
                    'item_id'   : item_id,
                    'date'      : data,
                    'price'     : preco
                }

                return jsonify(response)
            
            else:
                response = {
                    'error': 'Verifique se os campos estão sendo inseridos corretamente!'
                }

                return jsonify(response)
########################################  


### METÓDO GET PARA LISTAR UMA TRANSAÇÃO ESPECÍFICA ###
    @app.route('/transactions/<int:id>', methods=['GET'])
    def mostrar_transacao_especifico(id):
            
            cursor = conexao.cursor()
            
            recuperar_transacao_sql = f'SELECT * FROM transaction WHERE idtransaction = "{id}"'       
            cursor.execute(recuperar_transacao_sql)
            
            transacao = cursor.fetchall()
            cursor.close()

            transacao_json = [
                {
                    'id'        : u[0], 
                    'buyer_id'  : u[1], 
                    'saller_id' : u[2], 
                    'item_id'   : u[3], 
                    'date'      : u[4], 
                    'price'     : u[5]
                } 
                for u in transacao
            ]
            
            return jsonify(transacao_json)
######################################################

else:
    print("Não foi possível conectar com o MySql!!")

app.run(port=5000, host='localhost', debug=True)