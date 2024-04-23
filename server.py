from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json

app = Flask(__name__)

questions = ['']*10
solutions = [0]*10
questions[0] = "What dive direction does this diagram represent?"
solutions[0] = 4 # Question 1: What dive direction does this diagram represent? 4 = Inward
questions[1] = "Back dives start with which number?"
solutions[1] = 2 # Question 2: Back dives start with which number? 2
questions[2] = "The letter B represents which position?"
solutions[2] = 1 # Question 3: The letter B represents which position? 1 = Pike
questions[3] = 'What is the description for the dive “5333D"?'
solutions[3] = 4 # Question 4: What is the description for the dive “5333D”? 4 = Reverse one-and-a-half flips, one-and-a-half twists free
questions[4] = 'What is the dive number for the following dive description “Front triple tuck”?'
solutions[4] = 3 # Question 5: What is the dive number for the following dive description “Front triple tuck”? 3 = 106C
solutions[5] = 1 # Question 6: What dive direction does this diagram represent? 1 = Front
solutions[6] = 5 # Question 7: Twisting dives start with which number? 5
solutions[7] = 3 # Question 8: The letter D represents which position? 3 = Free
solutions[8] = "105B" # Question 9: What is the dive number for this dive? 203B
solutions[9] = "5132D" # Question 10: What is the dive number for this dive? 5132D


# Function to log page visits
def log_visit(page):
    visit = {
        'page': page,
        'timestamp': datetime.now().isoformat()
    }
    with open('page_visits.json', 'a') as f:
        f.write(json.dumps(visit) + '\n')

# Function to log quiz submissions
def log_submission(answers, score):
    submission = {
        'timestamp': datetime.now().isoformat(),
        'answers': answers,
        'score': score
    }
    with open('quiz_logs.json', 'a') as f:
        f.write(json.dumps(submission) + '\n')

# Clear the page_visits.json file when the server is started
open('page_visits.json', 'w').close()
open('quiz_logs.json', 'w').close()

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
    answers = []
    number_input1 = int(request.form['number-input1'])
    answers.append(number_input1)
    number_input2 = int(request.form['number-input2'])
    answers.append(number_input2)
    number_input3 = int(request.form['number-input3'])
    answers.append(number_input3)
    number_input4 = int(request.form['number-input4'])
    answers.append(number_input4)
    number_input5 = int(request.form['number-input5'])
    answers.append(number_input5)
    # number_input6 = int(request.form['number-input6'])
    # number_input7 = int(request.form['number-input7'])
    # number_input8 = int(request.form['number-input8'])
    # number_input9 = int(request.form['number-input9'])
    # number_input10 = int(request.form['number-input10'])

    score = 0
    if number_input1 == solutions[0]:
        score += 1
    if number_input2 == solutions[1]:
        score += 1
    if number_input3 == solutions[2]:
        score += 1
    if number_input4 == solutions[3]:
        score += 1
    if number_input5 == solutions[4]:
        score += 1
    # if number_input6 == solutions[5]:
    #     score += 1
    # if number_input7 == solutions[6]:
    #     score += 1
    # if number_input8 == solutions[7]:
    #     score += 1
    # if number_input9 == solutions[8]:
    #     score += 1
    # if number_input10 == solutions[9]:
    #     score += 1

    log_submission(answers, score)

    return render_template('quiz_results.html', number_input=score)

@app.route('/quiz_feedback')
def quiz_feedback():
    with open('quiz_logs.json', 'r') as f:
        last_submission = list(f)[-1]
    submission = json.loads(last_submission)
    return render_template('quiz_feedback.html', solutions=solutions, submission=submission)

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
