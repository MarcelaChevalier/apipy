from flask import Flask, jsonify, request, make_response
from flask_mysqldb import MySQL
from config import config
from validacao import *
from auth import auth_required
import pymysql

app = Flask(__name__)

conexao = MySQL(app)


@app.route('/', methods=['GET'])
@auth_required
def index():
    if request.authorization and request.authorization.username == 'funcionaria1' and request.authorization.password == '1234':
        return '<h1>Você está logado!</h1>'
    return make_response('Login/senha incorretos!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


@app.route('/produtos', methods=['GET'])
@auth_required
def lista_produtos():
    try:
        cursor = conexao.connection.cursor()
        sql = "SELECT idproduto, nome, preço, quantidade FROM produtos"
        cursor.execute(sql)
        dados = cursor.fetchall()
        produtos = []
        for fila in dados:
            novoproduto = {
                'idproduto': fila[0], 'nome': fila[1], 'preço': fila[2], 'quantidade': fila[3]}
            produtos.append(novoproduto)
        return jsonify({'produtos': produtos, 'Mensagem': "Produtos listados!", 'exito': True})
    except Exception as ex:
        print(ex)
        return jsonify({'Mensagem': "Erro", 'exito': False})


def produtos_db(idproduto):
    try:
        cursor = conexao.connection.cursor()
        sql = "SELECT idproduto, nome, preço, quantidade FROM produtos WHERE idproduto = '{0}'".format(
            idproduto)
        cursor.execute(sql)
        dados = cursor.fetchone()
        if dados != None:
            produtos = {'idproduto': dados[0], 'nome': dados[1],
                        'preço': dados[2], 'quantidade': dados[3]}
            return produtos
        else:
            return None
    except Exception as ex:
        raise ex


@app.route('/produto/<idproduto>', methods=['GET'])
@auth_required
def consultar_cliente(idproduto):
    try:
        produto = produtos_db(idproduto)
        if produto != None:
            return jsonify({'produto': produto, 'mensagem': "Produto encontrado.", 'exito': True})
        else:
            return jsonify({'mensagem': "Produto não encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensagem': "Error", 'exito': False})


@app.route('/novoproduto', methods=['POST'])
@auth_required
def cadastro_produto():
    if (validar_idproduto(request.json['idproduto']) and validar_nome(request.json['nome']) and validar_preço(
            request.json['preço']) and validar_quantidade(request.json['quantidade'])):
        try:
            cliente = produtos_db(request.json['idproduto'])
            if cliente != None:
                return jsonify({'mensagem': "Produto já existe, não  se pode duplicar.", 'exito': False})
            else:
                cursor = conexao.connection.cursor()
                sql = """INSERT INTO produtos (idproduto, nome, preço, quantidade) 
                VALUES ('{0}', '{1}', '{2}', '{3}')""".format(request.json['idproduto'], request.json['nome'], request.json['preço'], request.json['quantidade'])
            cursor.execute(sql)
            conexao.connection.commit()
            return jsonify({'Mensagem': "Produto cadastrado com sucesso!", 'exito': True})
        except Exception as ex:
            print(ex)
        return jsonify({'Mensagem': "Erro", 'exito': False})
    else:
        return jsonify({'mensagem': "Parámetros inválidos...", 'exito': False})


@app.route('/atualizarproduto/<idproduto>', methods=['PUT'])
@auth_required
def atualizar_produto(idproduto):
    if (validar_idproduto(request.json['idproduto']) and validar_nome(request.json['nome']) and validar_preço(
            request.json['preço']) and validar_quantidade(request.json['quantidade'])):
        try:
            produtos = produtos_db(request.json['idproduto'])
            if produtos != None:
                cursor = conexao.connection.cursor()
                sql = """UPDATE produtos SET nome ='{0}', preço ='{1}', quantidade ='{2}' WHERE  idproduto ='{3}'""".format(
                    request.json['nome'], request.json['preço'], request.json['quantidade'], idproduto)
                cursor.execute(sql)
                conexao.connection.commit()
                return jsonify({'mensagem:': 'Produto atualizado', 'exito': True})
            else:
                return jsonify({'mensagem': "Produto não encontrado.", 'exito': False})
        except Exception as ex:
            return jsonify({'mensagem': "Error", 'exito': False})
    else:
        return jsonify({'mensagem': "Parámetros inválidos...", 'exito': False})


@app.route('/deletarproduto/<idproduto>', methods=['DELETE'])
@auth_required
def apagar_produto(idproduto):
    try:
        produto = produtos_db(idproduto)
        if produto != None:
            cursor = conexao.connection.cursor()
            sql = "DELETE FROM produtos WHERE idproduto = '{0}'".format(
                idproduto)
            cursor.execute(sql)
            conexao.connection.commit()
            return jsonify({'mensagem': "Produto apagado.", 'exito': True})
        else:
            return jsonify({'mensagem': "Produto não encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensagem': "Error", 'exito': False})


def pagina_nao_encontrada(error):
    return "<h1> A página que está buscando, não existe :/ </h1>", 404


if __name__ == '__main__':
    app.config.from_object(config['desenvolvedor'])
    app.register_error_handler(404, pagina_nao_encontrada)
    app.run(port=5002)

# fetchall converter para ser entendido no python
