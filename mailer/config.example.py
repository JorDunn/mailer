class Config(object):
    DEBUG = True,
    TESTING = True,
    PONY = {
        'provider': 'mysql',
        'user': 'root',
        'password': 'changeme',
        'dbname': 'mailer'
    }
