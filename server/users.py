class Users:

    def __init__(self, *args, **kwargs):
        self._id = kwargs.get('_id', None)
        self.user = kwargs.get('user', None)
        self.salt = kwargs.get('salt', None)
        self.hash = kwargs.get('hash', None)
    
    def setId(self, _id):
        self._id = _id
    
    def setUser(self, user):
        self.user = user
    
    def setSalt(self, salt):
        self.salt = salt
    
    def setHash(self, hash):
        self.hash = hash
    
    def getId(self):
        return self._id
    
    def getUser(self):
        return self.user
    
    def getSalt(self):
        return self.salt
    
    def getHash(self):
        return self.hash
    
    def getInfo(self):
        return {'user': self.user, 'salt': self.salt, 'hash': self.hash}
    
    def getAll(self):
        return {'_id': self._id, 'user': self.user, 'salt': self.salt, 'hash': self.hash}