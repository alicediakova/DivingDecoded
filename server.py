from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json, random, csv, os

app = Flask(__name__)

# reads dive_numbers.csv and converts to datastructure (dict) where keys are dive numbers and 
# vals are dive descriptions -> used for making quiz more versatile, specifically for video questions
dive_numbers = {}
with open('dive_numbers.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        number = row[0].lower()
        desc = row[1]
        dive_numbers[number] = desc

# Specify the directory where the videos are stored
video_directory = 'static/videos'

# Get a list of all video titles
video_files = os.listdir(video_directory)

# Remove file extensions and '_slow' from 
# video titles to get dive numbers
video_dive_numbers = [f.replace('_slow.mov', '').replace('.mov', '') for f in video_files]
video_dive_numbers = set(video_dive_numbers)

# global current_questions
# current_questions = []

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
    # current_questions = []
    # Load questions from questions.json
    with open('questions.json') as f:
        all_questions = json.load(f)

    # Group questions by type
    questions_by_type = {'0': [], '1': [], '2': [], '3': []}
    for question in all_questions:
        questions_by_type[question['type']].append(question)

    # Select 2 random questions from each type, except for type "3" where you select 4
    questions = []
    selected_dives = set()
    for question_type in questions_by_type:
        if question_type == '3':
            type_3 = dict()
            for temp_question in random.sample(questions_by_type[question_type], 4):
                #print(temp_question)
                random_dive_number = random.choice(list(dive_numbers.keys()))
                while random_dive_number in selected_dives or random_dive_number not in video_dive_numbers:
                    random_dive_number = random.choice(list(dive_numbers.keys()))
                # at this point we have a unique dive number for this quiz
                selected_dives.add(random_dive_number)
                desc = dive_numbers[random_dive_number]

                # print(selected_dives)

                options = []
                answer = -1
                video = random_dive_number
                if temp_question['video'] == '_slow':
                    video += '_slow'
                video += '.mov'
                print(video)
                if 'description' in temp_question['question']:
                    # we want to add descriptions as options
                    # print('desc question')
                    #answer = desc
                    options.append(desc)
                    count = 0
                    while count < 3:
                        new_desc = random.choice(list(dive_numbers.values()))
                        if new_desc != desc and new_desc not in options:
                            options.append(new_desc)
                            count += 1
                    random.shuffle(options)
                    answer = options.index(desc)

                else:
                    # print('dive number question')
                    # we want to add dive numbers as options
                    #answer = random_dive_number.upper()
                    options.append(random_dive_number.upper())
                    count = 0
                    while count < 3:
                        new_dive_number = random.choice(list(dive_numbers.keys()))
                        if new_dive_number != random_dive_number and new_dive_number not in options:
                            options.append(new_dive_number.upper())
                            count += 1
                    random.shuffle(options)
                    answer = options.index(random_dive_number.upper())

                temp_question['video'] = video
                temp_question['answer'] = answer
                temp_question['options'] = options

                # print("Before temp_question block")
                # print(temp_question)
                # print(temp_question['id'])
                type_3[temp_question['id']] = temp_question  
                # print(type_3)

                # print(temp_question)
                questions.append(temp_question)

            # Load the data from the JSON file
            with open('questions.json', 'r') as f:
                data = json.load(f)

            # print(type_3)
            # print(type_3.keys())

            # Find the item with id = 14 and modify it
            for item in data:
                # print(item['id'])
                if item['id'] in type_3.keys():
                    # print(item)
                    temp_q = type_3[item['id']]
                    item['options'] = temp_q['options'] 
                    item['answer'] = temp_q['answer'] 
                    item['video'] = temp_q['video'] 

            # print(data)

            # Write the modified data back to the JSON file
            with open('questions.json', 'w') as f:
                json.dump(data, f, indent=4)
        else:
            questions += random.sample(questions_by_type[question_type], 2)


    # print(questions)
    # Render template with questions
    # current_questions = questions
    return render_template('quiz.html', questions=questions)


# want answers to look like: {id: {user answer, correct answer}...} -> where all elements are ints

@app.route('/quiz_results', methods=['POST'])
def quiz_results():
    log_visit('quiz_results')
    form_answers = request.form.to_dict()  # Get all form data

    #print(form_answers)

    answers = {}
    for key, val in form_answers.items():
        answers[int(key.replace('number-input', ''))] = [int(val)-1,-1]

    # Load questions from questions.json
    with open('questions.json') as f:
        all_questions = json.load(f)

    # Get the correct answers
    # print(current_questions)
    correct_answers = {q['id']: q['answer'] for q in all_questions}
    #print(correct_answers)

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
