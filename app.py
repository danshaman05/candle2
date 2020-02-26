from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/about')
def hello_daniel():
    return 'About page!'

if __name__ == '__main__':
    app.run()
