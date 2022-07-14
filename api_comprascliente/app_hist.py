from urllib import response
from webbrowser import get
from xml.dom.minidom import Identified
from flask import Flask, jsonify, request, make_response
from flask_mysqldb import MySQL
from config import config
from validacao import *
from auth import auth_required
import pymysql
import json
import requests

app = Flask(__name__)

conexao = MySQL(app)


@app.route('/', methods=['GET'])
@auth_required
def index():
    if request.authorization and request.authorization.username == 'funcionaria1' and request.authorization.password == '1234':
        return '<h1>Você está logado!</h1>'
    return make_response('Login/senha incorretos!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


@app.route('/historico', methods=['GET'])
@auth_required
def historico_clientes():
    try:
        cursor = conexao.connection.cursor()
        sql = "SELECT idhistorico, idproduto, idcliente FROM historico"
        cursor.execute(sql)
        dados = cursor.fetchall()
        produtos = []
        for fila in dados:
            historico = {
                'idhistorico': fila[0], 'idproduto': fila[1], 'idcliente': fila[2]}
            produtos.append(historico)
        return jsonify({'historico': produtos, 'Mensagem': "Historico listado!", 'exito': True})
    except Exception as ex:
        print(ex)
        return jsonify({'Mensagem': "Erro", 'exito': False})


def historico_db(idhistorico):
    try:
        cursor = conexao.connection.cursor()
        sql = "SELECT idhistorico, idproduto, idcliente FROM historico WHERE idhistorico = '{0}'".format(
            idhistorico)
        cursor.execute(sql)
        dados = cursor.fetchone()
        if dados != None:
            historico = {'idhistorico': dados[0], 'idproduto': dados[1],
                         'idcliente': dados[2]}
            return historico
        else:
            return None
    except Exception as ex:
        raise ex


@app.route('/produto/<idhistorico>', methods=['GET'])
@auth_required
def historico_cliente(idhistorico):
    try:
        historico = historico_db(idhistorico)
        if historico != None:
            return jsonify({'historico': historico, 'mensagem': "Historico encontrado.", 'exito': True})
        else:
            return jsonify({'mensagem': "Historico não encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensagem': "Error", 'exito': False})


@app.route('/novohistorico', methods=['POST'])
@auth_required
def novo_historico():
    if (validar_idhistorico(request.json['idhistorico']) and validar_idproduto(request.json['idproduto']) and validar_idcliente(
            request.json['idcliente'])):
        try:
            historico = historico_db(request.json['idhistorico'])
            if historico != None:
                return jsonify({'mensagem': "Historico já existe, não  se pode duplicar.", 'exito': False})
            else:
                cursor = conexao.connection.cursor()
                sql = """INSERT INTO historico (idhistorico, idproduto, idcliente) 
                VALUES ('{0}', '{1}', '{2}')""".format(request.json['idhistorico'], request.json['idproduto'], request.json['idcliente'])
            cursor.execute(sql)
            conexao.connection.commit()
            return jsonify({'Mensagem': "Historico cadastrado com sucesso!", 'exito': True})
        except Exception as ex:
            print(ex)
        return jsonify({'Mensagem': "Erro", 'exito': False})
    else:
        return jsonify({'mensagem': "Parámetros inválidos...", 'exito': False})


@app.route('/atualizarhistorico/<idhistorico>', methods=['PUT'])
@auth_required
def atualizar_historico(idhistorico):
    if (validar_idhistorico(request.json['idhistorico']) and validar_idproduto(request.json['idproduto']) and validar_idcliente(
            request.json['idcliente'])):
        try:
            produtos = historico_db(request.json['idhistorico'])
            if produtos != None:
                cursor = conexao.connection.cursor()
                sql = """UPDATE historico SET idproduto ='{0}', idcliente ='{1}'WHERE  idhistorico ='{2}'""".format(
                    request.json['idproduto'], request.json['idcliente'], idhistorico)
                cursor.execute(sql)
                conexao.connection.commit()
                return jsonify({'mensagem:': 'Historico atualizado', 'exito': True})
            else:
                return jsonify({'mensagem': "Histórico não encontrado.", 'exito': False})
        except Exception as ex:
            return jsonify({'mensagem': "Error", 'exito': False})
    else:
        return jsonify({'mensagem': "Parámetros inválidos...", 'exito': False})


@app.route('/deletarhistorico/<idhistorico>', methods=['DELETE'])
@auth_required
def apagar_historico(idhistorico):
    try:
        historico = historico_db(idhistorico)
        if historico != None:
            cursor = conexao.connection.cursor()
            sql = "DELETE FROM historico WHERE idhistorico = '{0}'".format(
                idhistorico)
            cursor.execute(sql)
            conexao.connection.commit()
            return jsonify({'mensagem': "Historico apagado.", 'exito': True})
        else:
            return jsonify({'mensagem': "Historico não encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensagem': "Error", 'exito': False})



@app.route('/catalogo/inventario/<idproduto>')
def invetario_catalogo(idproduto):
    clienteend = requests.get(
        'http://127.0.0.1:5002/produtos', auth=("funcionaria1", "1234"))
    text = clienteend.text
    data = (json.loads(text))
    produtos = data['produtos']
    response = {}
    lista = []

    for produto in produtos:
        if produto['idproduto'] == int(idproduto):
            lista.append(produto)
    try:
        cursor = conexao.connection.cursor()
        sql = "SELECT idhistorico, idproduto, idcliente FROM historico WHERE idproduto= '{0}'".format(
            idproduto)
        cursor.execute(sql)
        cliRow = cursor.fetchall()
        response['Invetário'] = cliRow
        response['Produto'] = lista
        return response
    except Exception as e:
        print(e)


@app.route('/cliente/inventario/<idcliente>')
def invetario_cliente(idcliente):
    clienteend = requests.get(
        'http://127.0.0.1:5000/clientes', auth=("funcionaria1", "1234"))
    text = clienteend.text
    data = (json.loads(text))
    cliente = data['clientes']
    response = {}
    lista = []

    for clientes in cliente:
        if clientes['id'] == int(idcliente):
            lista.append(clientes)
            
    try:
        cursor = conexao.connection.cursor()
        sql = "SELECT idhistorico, idproduto, idcliente FROM historico WHERE idcliente= '{0}'".format(
            idcliente)
        cursor.execute(sql)
        cliRow = cursor.fetchall()
        response['Invetário'] = cliRow
        response['Cliente'] = lista
        return response
    except Exception as e:
        print(e)
        




@app.route ('/clientes/inventario/<idcliente>')
def inventario_cliente_catalogo(idcliente):
    

        cursor = conexao.connection.cursor()
        sql = "SELECT idhistorico, idcliente, idproduto FROM historico WHERE idcliente = '{}'".format(idcliente)
        cursor.execute(sql)
        cliRow = cursor.fetchall()
        cliente_inventario = requests.get("http://127.0.0.1:5000/clientes/{}".format(idcliente), auth=("funcionaria1", "1234"))
        text = cliente_inventario.text
        data = json.loads(text)
        clientes = data['cliente']
        lista2=[]
        
        for compra in cliRow:
            
            
            produto_inventario = requests.get("http://127.0.0.1:5002/produto/{}".format(compra[2]), auth=("funcionaria1", "1234"))
            text1 = produto_inventario.text
            data1 = json.loads(text1)
            lista2.append(data1)
            print(data1)
            
        try:
            response={}
            cursor = conexao.connection.cursor()
            sql3 = "SELECT * FROM historico WHERE idcliente = '{0}'".format(idcliente)
            cursor.execute(sql3)
            cliRow2 = cursor.fetchall()
            response['Inventário'] = cliRow2
            response['Cliente'] = clientes
            response['Produto'] = lista2
            return response

        except Exception as e:
            print (e)



        
              
def pagina_nao_encontrada(error):
    return "<h1> A página que está buscando, não existe :/ </h1>", 404


if __name__ == '__main__':
    app.config.from_object(config['desenvolvedor'])
    app.register_error_handler(404, pagina_nao_encontrada)
    app.run(port=5003)
