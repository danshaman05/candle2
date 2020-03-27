from candle_backend import app

'''
Autor: Daniel Grohol
Project: Candle2 (Candle rewrite from PHP to Python)
 In this project I am reading data from MySQL DB and processing them and printing in same format as in old Candle. 
'''


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)



