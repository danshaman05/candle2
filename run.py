from candle_backend import create_app

'''
Project: Candle2 (Candle rewrite from PHP to Python)
Autor: Daniel Grohol
'''

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
