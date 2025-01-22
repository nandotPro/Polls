import jwt
from datetime import datetime, timedelta
from typing import Dict
import os

class JWTHandler:
    def __init__(self):
        self.secret = os.getenv("JWT_SECRET")
        self.algorithm = "HS256"
        self.expiration = timedelta(days=1)

    def generate_token(self, payload: Dict) -> str:
        """Gera um novo token JWT"""
        exp = datetime.utcnow() + self.expiration
        payload["exp"] = exp
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def validate_token(self, token: str) -> Dict:
        """Valida um token JWT e retorna o payload"""
        try:
            return jwt.decode(token, self.secret, algorithms=[self.algorithm])
        except jwt.ExpiredSignatureError:
            raise ValueError("Token expirado")
        except jwt.InvalidTokenError:
            raise ValueError("Token inválido") 