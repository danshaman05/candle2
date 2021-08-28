'''
Project: Candle (New Generation): Candle rewrite from PHP to Python.
Author: Daniel Grohol
'''
from candle import create_app


app = create_app()

if __name__ == '__main__':
    app.run(use_reloader=True)
