# import data 
import pickle
from flask_cors import CORS
from flask import Flask, render_template, request, json, jsonify

app = Flask(__name__)
CORS(app)
score_delhi=pickle.load(open('E:/Sem6/BTP-sem6/btp_notebooks/score_delhi1.pkl','rb'))
score_bangalore=pickle.load(open('score_bangalore.pkl','rb'))

# print(score_bangalore[1])

@app.route("/")
@app.route('/home')
@app.route('/delhi')
def home():
    return render_template('delhi_leaf.html')

@app.route('/testdelhi')
def testdelhi():
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
    return render_template('bangalore_leaf.html')


@app.route('/testbangalore')
def testbangalore():
    return render_template('bangalore.html')

@app.route('/getScoreBangalore')
def getScoreBangalore():
    print(type(request.args['Ward_No']))
    data=score_bangalore.get(int(request.args['Ward_No']),{})
    # print(data)
    return jsonify(data)

@app.route('/info')
def info():
    return render_template('info.html')

if __name__=='__main__':
    app.run(debug=True)

