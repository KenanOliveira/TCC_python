from app import jsonify, app, mongo, request, cross_origin, ASCENDING, DESCENDING
from videos import Videos
from bson import json_util, ObjectId
import json
from users import Users
import hashlib, uuid
import jwt
import datetime
from functools import wraps
import itertools

#
#
# Autorização
def user_by_username(username):
    try:
        return mongo.db.users.find_one({'user': username})
    except:
        return None

def check_password_hash(senha, user):

    try:
        busca = mongo.db.users.find_one({'user': user})
    except:
        return None
    
    hash = hashlib.sha512(senha.encode('utf-8') + busca['salt'].encode('utf-8')).hexdigest()

    if busca['hash'] == hash:
        return True
    else:
        return None

def auth(senha, username):
    # auth = request.authorization
    if not senha or not username:
        return jsonify({'result': 'Não identificado', 'WWW-Authenticate': 'Basic auth="Login required"'}), 401
    
    user = user_by_username(username)

    if not user:
        return jsonify({'result': 'usuário não encontrado', 'data': {}}), 401
    
    if user and check_password_hash(senha, username):
        token = jwt.encode({'user': username, 'exp': datetime.datetime.now() + datetime.timedelta(hours=12)}, app.config['SECRET_KEY'])

        return jsonify({'result': 'sucesso', 'token': token.decode('utf-8'), 'exp': datetime.datetime.now() + datetime.timedelta(hours=12)})
    
    return jsonify({'result': 'Não identificado', 'WWW-Authenticate': 'Basic auth="Login required"'}), 401

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers['Authorization']
        token = token.replace('Bearer ', '')
        # print(app.config['SECRET_KEY'])
        if not token:
            return jsonify({'result': 'token inválido', 'data': {}}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            user_by_username(username=data['user'])
        except:
            return jsonify({'result': 'token invalido ou expirado', 'data': {}}), 401
        return f(*args, **kwargs)
    return decorated

#
#
# Insere novos vídeos
@app.route('/inserir', methods=['POST'])
@cross_origin()
@token_required
def inicio(*args):
    video = Videos()
    video.setTitulo(request.json['titulo'])
    video.setDescricao(request.json['descricao'])
    video.setLink(request.json['link'])
    video.setTags(request.json['tags'])
    video.setDataPublicacao(request.json['dataPublicacao'])

    try:
        mongo.db.videos.insert_one({'titulo': video.getTitulo(), 'descricao': video.getDescricao(), 'link':video.getLink(),'linkImg':video.createLinkImage(video.getLink()), 'tags': video.getTags(), 'dataPublicacao': video.getDataPublicacao()})
        return jsonify({'result': 'Sucesso'}), 200
    except:
        return jsonify({'result': 'algo deu errado :('}), 500

# Busca todos os vídeos
@app.route('/buscaTodos', methods=['GET'])
@cross_origin()
# @token_required
def buscaTodos(*args):
    videos = mongo.db.videos

    out = []

    for v in videos.find():
        _id = json.loads(json_util.dumps(v['_id']))
        _id = _id['$oid']
        out.append({'_id': _id, 'titulo': v['titulo'], 'descricao': v['descricao'], 'link':v['descricao'],'linkImg':v['linkImg'], 'tags': v['tags'], 'dataPublicacao': v['dataPublicacao'], 'atualizado': None})
    
    if len(out) > 0:
        return jsonify({'result': out})
    else:
        return jsonify({'result': []})

# Busca Itens Inicio
@app.route('/buscaInicio', methods=['GET'])
@cross_origin()
# @token_required
def buscaInicio(*args):
    videos = mongo.db.videos

    out = []

    for v in videos.find().sort('dataPublicacao', DESCENDING).limit(4):
        _id = json.loads(json_util.dumps(v['_id']))
        _id = _id['$oid']
        out.append({'_id': _id, 'titulo': v['titulo'], 'descricao': v['descricao'], 'link':v['descricao'],'linkImg':v['linkImg'], 'tags': v['tags'], 'dataPublicacao': v['dataPublicacao'], 'atualizado': None})
    
    if len(out) > 0:
        return jsonify({'result': out})
    else:
        return jsonify({'result': []})

# Busca um vídeo pelo ID
@app.route('/buscaUnico/<id>', methods=['GET'])
@cross_origin()
# @token_required
def buscaUnico(id, *args):
    try:
        busca = mongo.db.videos.find_one({'_id': ObjectId(id)})
        # print(busca)
        video = Videos()
        _id = json.loads(json_util.dumps(busca['_id']))
        _id = _id['$oid']
        video.setId(_id)
        video.setTitulo(busca['titulo'])
        video.setDescricao(busca['descricao'])
        video.setLink(busca['link'])
        video.setLinkImg(busca['linkImg'])
        video.setTags(busca['tags'])
        video.setDataPublicacao(busca['dataPublicacao'])

        if video:
            return jsonify({'result': video.getAll()}), 200
        else:
            return jsonify({'result': 'Nada por aqui'}), 404
    except:
        if busca == None:
            return jsonify({'result': 'Nada encontrado'}), 404
        else:
            return jsonify({'result': 'Erro no Banco de Dados'}), 500

# Atualiza o vídeo pelo ID
@app.route('/atualizaVideo/<id>', methods=['PUT'])
@cross_origin()
@token_required
def atualizaVideo(id, *args):
    video = Videos()
    video.setTitulo(request.json['titulo'])
    video.setDescricao(request.json['descricao'])
    video.setLink(request.json['link'])
    video.setTags(request.json['tags'])
    # video.setDataPublicacao(request.json['dataPublicacao'])
    video.setAtualizado(request.json['atualizado'])

    try:
        mongo.db.videos.find_one_and_update({'_id': ObjectId(id)}, {'$set': {'titulo': video.getTitulo(), 'descricao': video.getDescricao(), 'link':video.getLink(),'linkImg':video.createLinkImage(video.getLink()), 'tags': video.getTags(), 'atualizado': video.getAtualizado()}})
        return jsonify({'result': 'Sucesso'})
    except:
        return jsonify({'result': 'Erro'})

# Deleta um vídeo pelo ID
@app.route('/deletaVideo/<id>', methods=['DELETE'])
@cross_origin()
@token_required
def deletaVideo(id, *args):
    try:
        mongo.db.videos.find_one_and_delete({'_id': ObjectId(id)})
        return jsonify({'result': 'Sucesso'})
    except:
        return jsonify({'result': 'Erro'})

@app.route('/buscaResultados/<id>', methods=['GET'])
@cross_origin()
def buscaResultados(id):
    tags = mongo.db.videos.find({'tags': {'$regex': id}}).sort('dataPublicacao', DESCENDING)
    titulo = mongo.db.videos.find({'titulo': {'$regex': id}}).sort('dataPublicacao', DESCENDING)
    descricao = mongo.db.videos.find({'descricao': {'$regex': id}}).sort('dataPublicacao', DESCENDING)
    out = []

    for t in tags:
        out.append(t['_id'])

    for t in titulo:
        out.append(t['_id'])

    for t in descricao:
        out.append(t['_id'])
    
    newOut = list(dict.fromkeys(out))

    busca = mongo.db.videos.find({'_id': {"$in": newOut}})

    out = []
    for v in busca:
        _id = json.loads(json_util.dumps(v['_id']))
        _id = _id['$oid']
        out.append({'_id': _id, 'titulo': v['titulo'], 'descricao': v['descricao'], 'link':v['descricao'],'linkImg':v['linkImg'], 'tags': v['tags'], 'dataPublicacao': v['dataPublicacao'], 'atualizado': None})
    
    return jsonify({'result': out})

#
# 
#
# USER #
#
#

@app.route('/cadastrar', methods = ['POST'])
@cross_origin()
@token_required
def cadastrar(*args):
    user = Users()
    user.setUser(request.json['user'])

    try:
        busca = mongo.db.users.count_documents({'user': user.getUser()})
    except:
        return jsonify({'result': 'Erro'}), 500
        
    if busca >= 1:
        return jsonify({'result': 'Usuário já existe'}), 409
    else:
        senha = request.json['password']
        user.setSalt(uuid.uuid4().hex)
        user.setHash(hashlib.sha512(senha.encode('utf-8') + user.getSalt().encode('utf-8')).hexdigest())

        try:
            mongo.db.users.insert_one(user.getInfo())
            return jsonify({'result': 'Sucesso'})
        except:
            return jsonify({'result': 'Erro'}), 500

@app.route('/login', methods = ['POST'])
@cross_origin()
def login():
    pwd = request.json['password']
    user = request.json['user']

    return (auth(pwd, user))
    # return jsonify({'result': 'sucesso'})

# Erro 404, não encontrado
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': "erro"}), 404

# Inicia o app
if __name__ == '__main__':
    app.run()