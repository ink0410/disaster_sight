from app import create_app
from flask_swagger import swagger
from flask import jsonify

app = create_app()

@app.route('/')
def print_info():
	print('DSight')
	return jsonify('Fighting!')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
   