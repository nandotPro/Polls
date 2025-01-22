import bcrypt

class PasswordHandler:
    def hash_password(self, password: str) -> str:
        """Gera hash de uma senha"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt).decode()

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verifica se a senha corresponde ao hash"""
        return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())