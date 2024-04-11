from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/intro')
def intro():
    return render_template('intro.html')

@app.route('/positions')
def positions():
    return render_template('positions.html')

@app.route('/front')
def front():
    return render_template('front.html')

@app.route('/back')
def back():
    return render_template('back.html')

@app.route('/reverse')
def reverse():
    return render_template('reverse.html')

@app.route('/inward')
def inward():
    return render_template('inward.html')

@app.route('/twister')
def twister():
    return render_template('twister.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/quiz_results', methods=['POST'])
def quiz_results():
    number_input = int(request.form['number-input'])
    return render_template('quiz_results.html', number_input=number_input)

if __name__ == "__main__":
    app.run(debug=True)
