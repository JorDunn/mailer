from mailer.factory import create_app
from mailer.config import Config

if __name__ == '__main__':
    app = create_app()
    app.env = 'dev'
    app.debug = True
    app.run(host=Config.HOST, port=Config.PORT)
