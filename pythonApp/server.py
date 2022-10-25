from flask import Flask, render_template, jsonify, request
import folium
import json
from sqlalchemy import create_engine, text
import pandas as pd
from latent_factor import MatrixFactorization
from makeCSVfromDB import makeCsv


app = Flask(__name__)
'''app.config.from_pyfile('config.py')

database = create_engine(app.config['DB_URL'], encoding='utf-8')
app.database = database'''

@app.route('/lfcf', methods=['GET'])
def recommend_by_latent_factor():
    PATH = "../dataset/user-movie-ratings.csv"
    rating = pd.read_csv(PATH, sep=",", names=['placeID', 'userID', 'rating'])
    userId = request.args.get('userId') # userId=2
    userId = int(userId)
    visited = list(map(int, request.args.get('visited').split(',')))


    recommender = MatrixFactorization(R=rating, k=15)
    recommender.fit()
    result = recommender.recommend_places(userID=userId, maximum=15, threshold=3.5, visited=visited)
    # recommender.show_result()
    '''    user = app.database.execute(text("""
                                        SELECT * FROM users
                                        WHERE id = 1
                                        
                                        """))
    return jsonify(user)'''
    return jsonify({
        'result': result
    })

@app.route("/makecsv", methods=['GET'])
def utilityMatrix():
    makeCsv()
    return ""

@app.route("/data", methods=['GET'])
def hello_request():
    data = request.args.get('data')
    return jsonify(data)

if __name__ == "__main__":
    app.run()