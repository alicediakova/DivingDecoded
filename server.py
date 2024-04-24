from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json, random

app = Flask(__name__)


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
    # Load questions from questions.json
    with open('questions.json') as f:
        all_questions = json.load(f)

    # Group questions by type
    questions_by_type = {'0': [], '1': [], '2': []}
    for question in all_questions:
        questions_by_type[question['type']].append(question)

    # Select 2 random questions from each type
    questions = []
    for question_type in questions_by_type:
        questions += random.sample(questions_by_type[question_type], 2)

    # Render template with questions
    return render_template('quiz.html', questions=questions)


# want answers to look like: {id: {user answer, correct answer}...} -> where all elements are ints

@app.route('/quiz_results', methods=['POST'])
def quiz_results():
    log_visit('quiz_results')
    form_answers = request.form.to_dict()  # Get all form data

    answers = {}
    for key, val in form_answers.items():
        answers[int(key.replace('number-input', ''))] = [int(val)-1,-1]

    # Load questions from questions.json
    with open('questions.json') as f:
        all_questions = json.load(f)

    # Get the correct answers
    correct_answers = {q['id']: q['answer'] for q in all_questions}

    # Calculate score
    score = 0
    for key, val in answers.items():
        user_answer = val[0]
        if correct_answers[key] == user_answer:
            score += 1
        answers[key][1] = correct_answers[key]

    log_submission(answers, score)

    # Render template with score
    return render_template('quiz_results.html', number_input=score)

@app.route('/quiz_feedback')
def quiz_feedback():
    # Load last submission from quiz_logs.json
    with open('quiz_logs.json', 'r') as f:
        last_submission = json.loads(list(f)[-1])

    # Load questions from questions.json
    with open('questions.json') as f:
        all_questions = json.load(f)

    # Filter questions to only include those in the answers keys
    answered_questions = [q for q in all_questions if str(q['id']) in last_submission['answers'].keys()]
    print(answered_questions)

    # Render template with last submission and answered questions
    return render_template('quiz_feedback.html', submission=last_submission, questions=answered_questions)

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
