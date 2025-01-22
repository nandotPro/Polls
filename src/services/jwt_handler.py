import jwt
from datetime import datetime, timedelta
from typing import Dict
import os
from dotenv import load_dotenv

class JWTHandler:
    def __init__(self):
        load_dotenv()  # Carrega as variáveis do .env
        self.secret = os.getenv("JWT_SECRET")
        self.algorithm = os.getenv("JWT_ALGORITHM", "HS256")
        expiration = int(os.getenv("JWT_EXPIRATION", "3600"))
        self.expiration = timedelta(seconds=expiration)

    def generate_token(self, payload: Dict) -> str:
        """Gera um novo token JWT"""
        exp = int((datetime.now() + self.expiration).timestamp())
        payload = payload.copy()  # Não modificar o payload original
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