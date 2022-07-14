from flask import Flask, jsonify, request, make_response
from flask_mysqldb import MySQL
from config_end import config_end
import json
from auth import auth_required


app = Flask(__name__)

conexao=MySQL(app)



@app.route('/', methods=['GET'])
@auth_required
def index():
    if request.authorization and request.authorization.username == 'funcionaria1' and request.authorization.password == '1234':
        return '<h1>Você está logado!</h1>'
    return make_response('Login/senha incorretos!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})




@app.route('/enderecos', methods=['GET']) 
@auth_required
def listar_endereco():
    
    try:
        cursor = conexao.connection.cursor()
        sql = 'SELECT id, nome_endereco, logradouro, numero, bairro, cidade, uf, país,cep, id_end FROM endereco'
        cursor.execute(sql)
        
        dados=cursor.fetchall()
        todos_enderecos=[]
        for fila in dados:
            enderecos={'id':fila[0],'nome_endereco':fila[1],'logradouro':fila[2],'numero':fila[3],'bairro':fila[4],'cidade':fila[5],'uf':fila[6],'país':fila[7],'cep':fila[8], 'id_end':fila[9]}
            todos_enderecos.append(enderecos)
        return jsonify({'todos_enderecos': todos_enderecos, 'Mensagem': "Lista de endereços!"})
    except Exception as ex:
        print(ex)
        return jsonify ({'Mensagem': "Erro",  'exito': False})


def ler_endereco_delete(id_end): 
    try:
        cursor = conexao.connection.cursor()
        sql = "SELECT id, nome_endereco, logradouro, numero, bairro, cidade, uf, país, cep, id_end  FROM endereco WHERE id_end = '{0}'".format(id_end)
        cursor.execute(sql)
        dados = cursor.fetchone()
        if dados != None:
            enderecos={'id':dados[0],'nome_endereco':dados[1],'logradouro':dados[2],'numero':dados[3],'bairro':dados[4],'cidade':dados[5],'uf':dados[6],'país':dados[7],'cep':dados[8], 'id_end':dados[9]}
            return enderecos
        else:
            return None
    except Exception as ex:
        raise ex

def ler_endereco_delete2(id): 
    try:
        cursor = conexao.connection.cursor()
        sql = "SELECT id, nome_endereco, logradouro, numero, bairro, cidade, uf, país, cep, id_end  FROM endereco WHERE id = '{0}'".format(id)
        cursor.execute(sql)
        dados = cursor.fetchone()
        if dados != None:
            enderecos={'id':dados[0],'nome_endereco':dados[1],'logradouro':dados[2],'numero':dados[3],'bairro':dados[4],'cidade':dados[5],'uf':dados[6],'país':dados[7],'cep':dados[8], 'id_end':dados[9]}
            return enderecos
        else:
            return None
    except Exception as ex:
        raise ex


def ler_endereco_outro(id_end): 
    try:
        cursor = conexao.connection.cursor()
        sql = "SELECT id, nome_endereco, logradouro, numero, bairro, cidade, uf, país, cep, id_end FROM endereco WHERE id_end= '{0}'".format(id_end)
        cursor.execute(sql)
        dados = cursor.fetchone()
        if dados != None:
            enderecos={'id':dados[0],'nome_endereco':dados[1],'logradouro':dados[2],'numero':dados[3],'bairro':dados[4],'cidade':dados[5],'uf':dados[6],'país':dados[7],'cep':dados[8], 'id_end':dados[9]}
            return enderecos
        else:
            return None
    except Exception as ex:
        raise ex


@app.route('/enderecos/<id>', methods=['GET']) 
@auth_required
def ler_endereco_individual(id):
    try:
        cursor = conexao.connection.cursor()
        sql = "SELECT id, nome_endereco, logradouro, numero, bairro, cidade, uf, país, cep, id_end FROM endereco WHERE id = '{0}'".format(id)
        cursor.execute(sql)
        dados=cursor.fetchone()
        if dados != None:
            enderecos={'id':dados[0],'nome_endereco':dados[1],'logradouro':dados[2],'numero':dados[3],'bairro':dados[4],'cidade':dados[5],'uf':dados[6],'país':dados[7],'cep':dados[8], 'id_end':dados[9]}
            return jsonify({'enderecos': enderecos, 'Mensagem': "Endereco Encontrado."})
        else:
            return jsonify({'Mensagem': "Endereço não encontrado!"})
    except Exception as e:
        reponse = jsonify({"Message": f"{e}"})



@app.route('/novoendereco', methods= ['POST']) 
@auth_required
def registrar_endereco():
    try:
            cursor = conexao.connection.cursor()
            sql = """INSERT INTO endereco (id, nome_endereco, logradouro, numero, bairro, cidade, uf, país, cep) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}')""".format(request.json['id'], request.json['nome_endereco'], request.json['logradouro'], request.json['numero'], request.json['bairro'], request.json['cidade'], request.json['uf'], request.json['país'], request.json['cep'])
            cursor.execute(sql)
            conexao.connection.commit() 
            return jsonify({'mensagem:': 'Endereço cadastrado com sucesso!','exito': True})
  
    except Exception as ex:
        print(ex)
        return jsonify ({'Mensagem': "Erro",  'exito': False})



@app.route('/atualizarendereco/<id_end>', methods=['PUT']) 
@auth_required
def atualizar_endereco(id_end):
    try:
        endereco = ler_endereco_outro(request.json['id_end'])
        if endereco != None:
            cursor = conexao.connection.cursor()
            sql = """UPDATE endereco SET id = '{0}', nome_endereco = '{1}', logradouro = '{2}', numero = '{3}', bairro = '{4}', cidade = '{5}', uf = '{6}', país = '{7}', cep = '{8}' WHERE  id_end ='{9}'""".format(request.json['id'],request.json['nome_endereco'], request.json['logradouro'], request.json['numero'], request.json['bairro'], request.json['cidade'], request.json['uf'], request.json['país'], request.json['cep'],  id_end)
            cursor.execute(sql)
            conexao.connection.commit() 
            return jsonify({'mensagem:': 'Endereço atualizado com sucesso!','exito': True })
        else:
            return jsonify({'mensagem': "ID não encontrado.", 'exito': False})
    except Exception as e:
     reponse = jsonify({"Message": f"{e}"})

    return reponse




@app.route('/deletarendereco/<id_end>', methods=['DELETE'])
@auth_required
def deletar_endereco(id_end):
    try:
        endereco = ler_endereco_delete(id_end)
        if endereco != None:
                cursor = conexao.connection.cursor()
                sql = "DELETE FROM endereco WHERE id_end ='{0}'".format(id_end)
                cursor.execute(sql)
                conexao.connection.commit() 
                return jsonify({'mensagem': "Endereço excluído com sucesso.",  'exito': True})
        else:
            return jsonify({'mensagem': " Não encontrado.", 'exito': False})
    except Exception as e:
                reponse = jsonify({"Message": f"{e}"})

@app.route('/deletarenderecoid/<id>', methods=['DELETE'])
@auth_required
def deletar_endereco2(id):
    try:
        end = deletar_endereco(id)
        if end != None:
                cursor = conexao.connection.cursor()
                sql = "DELETE FROM endereco WHERE id ='{0}'".format(id)
                cursor.execute(sql)
                conexao.connection.commit() 
                return jsonify({'mensagem': "Endereço excluído com sucesso.",  'exito': True})
        else:
            return jsonify({'mensagem': " Não encontrado.", 'exito': False})
    except Exception as e:
            reponse = jsonify({"Message": f"{e}"})

def pagina_nao_encontrada(error):
    return '<h1>Página não encontrada</h1>', 404





    


if __name__=='__main__':
    app.config.from_object(config_end['desenvolvedor'])
    app.register_error_handler(404, pagina_nao_encontrada)
    app.run(port=5001)
