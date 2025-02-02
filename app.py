from flask import Flask
from api.main import blueprint as main_blueprint

app = Flask(__name__)

app.register_blueprint(main_blueprint)

app.secret_key = "6BtdCaEka6xjV4DVNxZ3pZB8mXJ70sig"

# Vercel requires the app to be named 'app'
app.debug = False

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)