from dotenv import load_dotenv
import os
load_dotenv() 

class Settings():

    def __init__(self,
                 database_hostname:str,
                 database_port:str,
                 database_password:str,
                 database_name:str,
                database_username: str,
                secret_key:str,
                algorithm: str,
                access_token_expire_minutes: int
                 ):
        self.database_hostname = database_hostname
        self.database_port = database_port
        self.database_password = database_password
        self.database_name = database_name
        self.database_username = database_username
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = int(access_token_expire_minutes)

settings = Settings(
    os.environ['DB_HOST'],
    os.environ['DB_PORT'],
    os.environ["DB_PASSWORD"],
    os.environ['DB_NAME'],
    os.environ['DB_USERNAME'],
    os.environ['SECRET_KEY'],
    os.environ['ALGORITHM'],
    os.environ['ACCESS_TOKEN_EXPIRE_MINUTES']
)