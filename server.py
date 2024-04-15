from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json

app = Flask(__name__)

# Function to log page visits
def log_visit(page):
    visit = {
        'page': page,
        'timestamp': datetime.now().isoformat()
    }
    with open('page_visits.json', 'a') as f:
        f.write(json.dumps(visit) + '\n')

# Clear the page_visits.json file when the server is started
open('page_visits.json', 'w').close()

@app.route('/')
def home():
    log_visit('homepage')
    return render_template('homepage.html')

@app.route('/intro')
def intro():
    log_visit('intro')
    return render_template('intro.html')

@app.route('/positions')
def positions():
    log_visit('positions')
    return render_template('positions.html')

@app.route('/front')
def front():
    log_visit('front')
    return render_template('front.html')

@app.route('/back')
def back():
    log_visit('back')
    return render_template('back.html')

@app.route('/reverse')
def reverse():
    log_visit('reverse')
    return render_template('reverse.html')

@app.route('/inward')
def inward():
    log_visit('inward')
    return render_template('inward.html')

@app.route('/twister')
def twister():
    log_visit('twister')
    return render_template('twister.html')

@app.route('/quiz')
def quiz():
    log_visit('quiz')
    return render_template('quiz.html')

@app.route('/quiz_results', methods=['POST'])
def quiz_results():
    log_visit('quiz_results')
    number_input = int(request.form['number-input'])
    return render_template('quiz_results.html', number_input=number_input)

@app.route('/visits')
def get_visits():
    with open('page_visits.json', 'r') as f:
        visits = [json.loads(line) for line in f]
    return jsonify(visits)

@app.route('/video/<dive_code>')
def video(dive_code):
    log_visit(f'video/{dive_code}')
    return render_template('video.html', dive_code=dive_code)

if __name__ == "__main__":
    app.run(debug=True)
