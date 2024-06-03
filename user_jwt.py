import jwt

def createToken(data:dict):
    token:str= jwt.encode(payload=data, key='misecret',algorithm='HS256')
    return token

def validateToken(token:str)->dict:
    data : dict= jwt.decode(token,key='misecret', algorithms=['HS256'])
    return data