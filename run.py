from mailer.factory import create_app

if __name__ == '__main__':
    app = create_app()
    app.env = 'dev'
    app.debug = True
    app.run(host='0.0.0.0')
