from passlib.context import CryptContext


SECRET_KEY = "RsKrje6KrCLwLe5neVGZLVNrQA4ttrYErHjR6X8iSZU"

ACCESS_TOKEN_EXPIRE_MINUTES = 1440

password_context = CryptContext(schemes=['bcrypt'], deprecated="auto")