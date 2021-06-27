import datetime
class Videos:

    def __init__(self, *args, **kwargs):
        self._id = kwargs.get('_id', None)
        self.titulo = kwargs.get('titulo', None)
        self.link = kwargs.get('link', None)
        self.linkImg = ''
        self.descricao = kwargs.get('descricao', None)
        self.tags = kwargs.get('tags', None)
        self.dataPublicacao = kwargs.get('dataPublicacao', None)
        self.atualizado = kwargs.get('atualizado', None)

    def setId(self, _id):
        self._id = _id

    def setTitulo(self, titulo):
        self.titulo = titulo
    
    def setLink(self, link):
        self.link = link[0:43].replace('watch?v=','embed/')
    
    def setLinkImg(self, linkImg):
        self.linkImg = linkImg
    
    def setDescricao(self, descricao):
        self.descricao = descricao
    
    def setTags(self, tags):
        self.tags = tags
    
    def setDataPublicacao(self, dataPublicacao):
        self.dataPublicacao = dataPublicacao
    
    def setAtualizado(self, atualizado):
        self.atualizado = atualizado
    
    def getId(self):
        # print(self._id)
        return self._id

    def getTitulo(self):
        return self.titulo
    
    def getLink(self):
        return self.link
    
    def getLinkImg(self):
        return self.linkImg
    
    def getDescricao(self):
        return self.descricao
    
    def getTags(self):
        return self.tags
    
    def getDataPublicacao(self):
        return self.dataPublicacao
    
    def getAtualizado(self):
        return self.atualizado
    
    def getAll(self):
        # print(self._id)
        return {'_id': self._id, 'titulo': self.titulo, 'descricao': self.descricao, 'link': self.link, 'linkImg': self.linkImg, 'tags': self.tags, 'dataPublicacao':self.dataPublicacao}
    
    def createLinkImage(self, link):
        try:
            ID = link.replace('https://www.youtube.com/embed/', '')
            linkImg = 'http://img.youtube.com/vi/'+ID+'/maxresdefault.jpg'
            return linkImg
        except:
            return None