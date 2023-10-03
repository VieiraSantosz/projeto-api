1° Criar banco de dados no MySql
- CREATE DATABASE SeboOnline;
- USE SeboOnline;


2° Criar a tabela user
- CREATE TABLE user (
    iduser INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(10) NOT NULL,
    email VARCHAR(30) NOT NULL,
    password VARCHAR(100) NOT NULL,
    status VARCHAR(10) NOT NULL,
    type VARCHAR(20) NOT NULL
);


3° Criar a tabela admin
- CREATE TABLE admin (
    idadmin INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(10) NOT NULL,
    email VARCHAR(30) NOT NULL,
    password VARCHAR(100) NOT NULL,
    status VARCHAR(10) NOT NULL,
    type VARCHAR(20) NOT NULL,
    date DATE NOT NULL,
    area VARCHAR(20) NOT NULL
);


4° Código para testar a conexão com o banco de dados
import mysql.connector

conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='vieira1234',
    database='seboonline',
)

if conexao.is_connected():
    print("Conexão ao MySQL bem-sucedida!")
    
else:
    print("Não foi possível conectar com o MySql!!")
    

### ADICIONA AS INFO NO BANCO DE DADOS ###
cursor = conexao.cursor()

nome    = "Vieira"
email   = "vieira@gmail.com"
senha   = "vieira1234"
status  = "ativo"
tipo    = "comprador"

comando = f'INSERT INTO usuarios (name, email, password, status, type) VALUES ("{nome}", "{email}", "{senha}", "{status}", "{tipo}")' 
cursor.execute(comando)

conexao.commit() # edita o seu banco de dados

cursor.close()
conexao.close()
#########################################


### LER AS INFO DO BANCO DE DADOS ###
cursor = conexao.cursor()

comando = 'SELECT * FROM usuarios' 
cursor.execute(comando)

resultado = cursor.fetchall() # lê o banco de dados
print(resultado)

cursor.close()
conexao.close()
#############################################


### MUDAR AS INFO DO BANCO DE DADOS ### 
cursor = conexao.cursor()

nome    = "Wesley"
senha   = "vieira1234"

comando = f'UPDATE usuarios SET name = "{nome}" WHERE password = "{senha}"' 
cursor.execute(comando)

conexao.commit() #edita o seu banco de dados

cursor.close()
conexao.close()
#########################################


### DELETAR AS INFO DO BANCO DE DADOS ###
cursor = conexao.cursor()

nome    = "Vieira"

comando = f'DELETE FROM usuarios WHERE name = "{nome}"' 
cursor.execute(comando)

conexao.commit() #edita o seu banco de dados

cursor.close()
conexao.close()
###########################################