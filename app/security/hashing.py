from passlib.context import CryptContext

# Initialize password hashing context using the secure bcrypt algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

class Hash:

    @staticmethod
    def bcrypt(password: str) -> str:
        """Hash a plain text password into a secure string for database storage."""
        return pwd_context.hash(password)

    @staticmethod
    def verify(plain_password: str, hashed_password: str) -> bool:
        """Verify if the input password matches the hashed password in the database."""
        return pwd_context.verify(plain_password, hashed_password)