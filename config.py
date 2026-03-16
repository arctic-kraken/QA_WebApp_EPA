import dotenv

class Config:
    db_url: str = dotenv.get_key(".env", "DB_CONNECT_URL")
    secret_key: str = dotenv.get_key(".env", "SECRET_KEY")
    hash_salt: str = dotenv.get_key(".env", "HASH_SALT")

    def __init__(self, db_url, secret_key, hash_salt):
        self.db_url = db_url
        self.secret_key = secret_key
        self.hash_salt = hash_salt

test_config = Config(
    db_url=dotenv.get_key("test.env", "DB_CONNECT_URL"),
    secret_key=dotenv.get_key("test.env", "SECRET_KEY"),
    hash_salt=dotenv.get_key("test.env", "HASH_SALT")
)