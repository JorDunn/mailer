from mailer.factory import create_app
from mailer.config import Config

app = create_app()

if __name__ == '__main__':
    app.env = Config.ENV
    app.debug = Config.DEBUG
    app.run(host=Config.HOST, port=Config.PORT)
