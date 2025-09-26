class config:
    SECRET_KEY = 'clave_secreta'

class DevelopmentConfig(config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD= ''
    MYSQL_DB = 'tpflask_aiup'

config = {
    'development': DevelopmentConfig
}