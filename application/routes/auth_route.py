from datetime import datetime, timedelta
from decouple import config
from fastapi import APIRouter
from fastapi.param_functions import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from hashlib import sha256
import jwt
from passlib.context import CryptContext

from application.api_security.auth import check
from application.models.ApiAuthSchema import Auth
from application.models.Response import Response
from infrastructure.DB import DB

JWT_SECRET = config('TOKEN_SECRET') 

router = APIRouter(
    tags=['Security'],
    prefix='/security'
)

class AuthHandler:
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = JWT_SECRET
    
    def get_password_hash(self, password):
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password, hashed_password):
        return check(sha256(bytearray(plain_password, 'utf-8')).hexdigest(), hashed_password)
    
    def encode_token(self, user):
        payload={
            'exp': datetime.utcnow() + timedelta(days=1),
            'iat': datetime.utcnow(),
            'sub': user
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )
        
    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms='HS256')
            return payload['sub']
        except jwt.exceptions.ExpiredSignatureError:
            return Response(401, {"MSG": "Signature expired"}, True)
        except jwt.InvalidTokenError:
            return Response(401, {"MSG": "Invalid token"}, True)
        
    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)
    
auth_handler = AuthHandler()
    
@router.post("/login")
def login(u: Auth):
    transaction = DB.login('iuser', u.username)
    if not transaction:
        return Response(400, {"MSG": "User not found"}, True)
    if len(transaction) > 0:
        if auth_handler.verify_password(u.password, transaction[0]):
            user = DB.read_one('iuser', f"user_email = '{u.username}'", "user_id, user_email,user_name, user_company, user_role, is_active", True)
            token = auth_handler.encode_token(user)
        else:
            return Response(403, {"MSG": "Invalid Credentials"}, True)
            
    return Response(200, {'token': token})