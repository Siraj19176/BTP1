# import data 
import pickle
from flask_cors import CORS
from flask import Flask, render_template, request, json, jsonify

app = Flask(__name__)
CORS(app)
score_delhi=pickle.load(open('score_delhi.pkl','rb'))
score_bangalore=pickle.load(open('score_bangalore.pkl','rb'))

# print(score_bangalore[1])

@app.route("/")
@app.route('/home')
@app.route('/delhi')
def home():
    return render_template('delhi.html')

@app.route('/getScoreDelhi')
def getScoreDelhi():
    data=score_delhi.get(request.args['Ward_No'], {})
    try:
        data['None']=data[None]
        del data[None]
    except:
        pass
    return jsonify(data)

@app.route('/bangalore')
def bangalore():
    return render_template('bangalore.html')

@app.route('/getScoreBangalore')
def getScoreBangalore():
    print(type(request.args['Ward_No']))
    data=score_bangalore.get(int(request.args['Ward_No']),{})
    # print(data)
    return jsonify(data)

if __name__=='__main__':
    app.run(debug=True)

