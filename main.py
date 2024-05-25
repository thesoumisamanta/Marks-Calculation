from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client['Marks']
marks_collection = db['average']

@app.route('/success')
def success():
    score = request.args.get('score', type=float)
    return f"You are selected in IIT KGP with the score of {score}"


@app.route('/failure')
def failure():
    score = request.args.get('score', type=float)
    return f"Sorry! Your Score is {score}, So Prepare for the next time"


@app.route('/', methods=['GET', 'POST'])
def calculate():
    if request.method == 'GET':
        return render_template('index.html')
    
    else:
        math = float(request.form['math'])
        physics = float(request.form['physics'])
        chemistry = float(request.form['chemistry'])

        average_marks = (math+physics+chemistry)/3

        average = {
            "math": math,
            "physics": physics,
            "chemistry": chemistry,
            "average": average_marks
        }

        marks_collection.insert_one(average)
        
        if average_marks>=90:
            return redirect(url_for('success', score=average_marks))
        else:
            return redirect(url_for('failure', score=average_marks))

        

        # return render_template('index.html', score=average_marks)

if __name__ == "__main__":
    app.run(debug=True)