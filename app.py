from flask import Flask,request,render_template,jsonify
import sys

from src.pipeline.predicting_pipeline import PredictPipeline
from src.exception import custom_exception

application=Flask(__name__)

app=application

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predictdata',methods=['GET','POST'])
def predict_movies():
    if request.method=='GET':
        return render_template('home.html')
    else:
        try:
            movie=request.json.get('movie')

            if not movie:
                return jsonify({"error":"please enter a movie!"}),400
            
            pipeline=PredictPipeline()
            res=pipeline.recommend(movie)
            if not res:
                return jsonify({"result":["sorry,no reccommendations found"]}),200
            
            return jsonify({"result":res})

        except Exception as e:
            raise custom_exception(e,sys)



if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
