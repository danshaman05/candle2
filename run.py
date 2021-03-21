from candle import create_app

'''
Project: Candle-NG (Candle rewrite from PHP to Python)
Author: Daniel Grohol
'''

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
