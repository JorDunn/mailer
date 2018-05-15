from typing import Dict, Any


class Config(object):
    DEBUG: bool = True
    TESTING: bool = True
    ENV: str = 'dev'
    HOST: str = "0.0.0.0"
    PORT: int = 5000
    SECRET_KEY: str = '7efee349137cf35be48087c8cfe153756fe0beafb44cc4d0'
    PONY: Dict[str, str] = {
        'provider': 'mysql',
        'user': 'username',
        'password': 'password',
        'dbname': 'mailer'
    }
    # The password must be an app specific password if using gmail
    EMAIL: Dict[str, Any] = {
        'host': 'smtp.domain.tld',
        'port': 465,
        'display': 'Some User',
        'username': 'email',
        'domain': 'domain.tld',
        'password': 'somepass'
    }
