
from flask import Flask, jsonify, request, make_response
from flask_mysqldb import MySQL
import requests
from config import config
from validacao import *
from auth import auth_required
import json


app = Flask(__name__)

conexao = MySQL(app)


@app.route('/', methods=['GET'])
@auth_required
def index():
    if request.authorization and request.authorization.username == 'funcionaria1' and request.authorization.password == '1234':
        return '<h1>Você está logado!</h1>'
    return make_response('Login/senha incorretos!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


@app.route('/clientes', methods=['GET'])
@auth_required
def lista_clientes():
    try:
        cursor = conexao.connection.cursor()
        sql = "SELECT id, nome, cpf, email, telefone, celular FROM cadastro"
        cursor.execute(sql)
        dados = cursor.fetchall()
        clientes_todos = []
        for fila in dados:
            novocliente = {'id': fila[0], 'nome': fila[1], 'cpf': fila[2], 'email': fila[3], 'telefone': fila[4],
                           'celular': fila[5]}
            clientes_todos.append(novocliente)
        return jsonify({'clientes': clientes_todos, 'Mensagem': "Clientes listados!", 'exito': True})
    except Exception as ex:
        print(ex)
        return jsonify({'Mensagem': "Erro", 'exito': False})


def clientes_db(id):
    try:
        cursor = conexao.connection.cursor()
        sql = "SELECT id, nome, cpf, email, telefone, celular FROM cadastro WHERE id = '{0}'".format(id)
        cursor.execute(sql)
        dados = cursor.fetchone()
        if dados != None:
            clientes = {'id': dados[0], 'nome': dados[1], 'cpf': dados[2], 'email': dados[3], 'telefone': dados[4],
                        'celular': dados[5]}
            return clientes
        else:
            return None
    except Exception as ex:
        raise ex


@app.route('/clientes/<id>', methods=['GET'])
@auth_required
def consultar_cliente(id):
    try:
        cliente = clientes_db(id)
        if cliente != None:
            return jsonify({'cliente': cliente, 'mensagem': "Cliente encontrado.", 'exito': True})
        else:
            return jsonify({'mensagem': "Cliente não encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensagem': "Error", 'exito': False})


@app.route('/novocliente', methods=['POST'])
@auth_required
def cadastro_cliente():
    if (validar_id(request.json['id']) and validar_nome(request.json['nome']) and validar_cpf(
            request.json['cpf']) and validar_email(request.json['email']) and validar_telefone(
            request.json['telefone']) and validar_celular(request.json['celular'])):
        try:
            cliente = clientes_db(request.json['id'])
            if cliente != None:
                return jsonify({'mensagem': "Cliente já existe, não  se pode duplicar.", 'exito': False})
            else:
                cursor = conexao.connection.cursor()
                sql = """INSERT INTO cadastro (id, nome, cpf, email, telefone, celular) 
                VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')""".format(request.json['id'], request.json['nome'],
                                                                            request.json['cpf'], request.json['email'],
                                                                            request.json['telefone'],
                                                                            request.json['celular'])
            cursor.execute(sql)
            conexao.connection.commit()
            return jsonify({'Mensagem': "Cliente cadastrado com sucesso!", 'exito': True})
        except Exception as ex:
            print(ex)
        return jsonify({'Mensagem': "Erro", 'exito': False})
    else:
        return jsonify({'mensagem': "Parámetros inválidos...", 'exito': False})


@app.route('/atualizar/<id>', methods=['PUT'])
@auth_required
def atualizar_cliente(id):
    if (validar_id(request.json['id']) and validar_nome(request.json['nome']) and validar_cpf(
            request.json['cpf']) and validar_email(request.json['email']) and validar_telefone(
            request.json['telefone']) and validar_celular(request.json['celular'])):
        try:
            cliente = clientes_db(request.json['id'])
            if cliente != None:
                cursor = conexao.connection.cursor()
                sql = """UPDATE cadastro SET nome ='{0}', cpf ='{1}', email ='{2}', 
                        telefone ='{3}', celular ='{4}' WHERE  id ='{5}'""".format(request.json['nome'],
                                                                                   request.json['cpf'],
                                                                                   request.json['email'],
                                                                                   request.json['telefone'],
                                                                                   request.json['celular'], id)
                cursor.execute(sql)
                conexao.connection.commit()
                return jsonify({'mensagem:': 'Cliente atualizado', 'exito': True})
            else:
                return jsonify({'mensagem': "Cliente não encontrado.", 'exito': False})
        except Exception as ex:
            return jsonify({'mensagem': "Error", 'exito': False})
    else:
        return jsonify({'mensagem': "Parámetros inválidos...", 'exito': False})


@app.route('/deletar/<id>', methods=['DELETE'])
@auth_required
def apagar_cliente(id):
    apagar=  requests.delete("http://127.0.0.1:5001/deletarenderecoid/{}".format(id), auth= ("funcionaria1", "1234"))
    
   
    try:
        
        
        if apagar != None:
            
            cursor = conexao.connection.cursor()
            sql = "DELETE FROM cadastro WHERE id = '{0}'".format(id)
            cursor.execute(sql)
            conexao.connection.commit()
           
            
            return jsonify({'mensagem': "Cliente apagado.", 'exito': True})
        else:
            return jsonify({'mensagem': "Cliente não encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensagem': "Error", 'exito': False})


@app.route ('/cliente/enderecos/<id>')
def endereco_cliente(id):
    clienteend = requests.get('http://127.0.0.1:5001/enderecos', auth= ("funcionaria1", "1234"))
    text = clienteend.text
    data = (json.loads(text))
    enderecos = data['todos_enderecos']
    response = {}
    lista = []
    for endereco in enderecos:
        if endereco['id'] == int(id):
            lista.append(endereco)

    try:
        
        cursor = conexao.connection.cursor()
        sql = "SELECT id, nome, email, cpf, telefone, celular FROM cadastro WHERE id = '{0}'".format(id)
        cursor.execute(sql)
        cliRow = cursor.fetchall()
        response['Cliente'] = cliRow[0]
        response['Endereços'] = lista
        return response
    except Exception as e:
       return jsonify({'mensagem': "Cliente e Endereço não localizado"})



def pagina_nao_encontrada(error):
    return "<h1> A página que está buscando, não existe :/ </h1>", 404


if __name__ == '__main__':
    app.config.from_object(config['desenvolvedor'])
    app.register_error_handler(404, pagina_nao_encontrada)
    app.run()

# fetchall converter para ser entendido no python
