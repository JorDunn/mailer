class Config(object):
    DEBUG = True
    TESTING = True
    ENV = 'dev'
    HOST = "0.0.0.0"
    PORT = 5000
    # SECRET_KEY should be changed before mailer is used in production.
    SECRET_KEY = '7efee349137cf35be48087c8cfe153756fe0beafb44cc4d0'
    # PONY vars should be changed before production too.
    PONY = {
        'provider': 'mysql',
        'user': 'someuser',
        'password': 'changeme',
        'dbname': 'mailer'
    }
