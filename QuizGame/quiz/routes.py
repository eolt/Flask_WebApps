from flask import render_template, request, redirect, url_for, flash
from quiz import app
import random
import json

# Opening JSON file
f = open('quiz/DB.json')

# return JSON object as a dictionary
data = json.load(f)

questions = data


@app.route('/')
@app.route('/home')
def index_page():
    random.shuffle(questions)
    return render_template('index.html')


@app.route("/question/<score>/<it>", methods=["GET", "POST"])
def question_page(score, it):
    if request.method == "POST":
        if next(iter(request.form.to_dict())) == 'True':
            if it != '4':
                flash('Correct!', category='success')
            score = int(score) + 1
        else:
            if it != '4':
                flash('Incorrect!', category='danger')

        it = int(it) + 1

        if int(it) < 5:
            return redirect(url_for('question_page', score=score, it=it))
        else:
            return redirect(url_for('end_page', score=score))

    if request.method == "GET":
        question_text = questions[int(it)]['question']
        answers = questions[int(it)]['answers']
        return render_template('question.html', question=question_text, answers=answers,
                               question_num=(int(it)+1), num_answers=len(answers), score=score)


@app.route("/end/<score>")
def end_page(score):
    percentage = (int(score) / 5) * 100
    return render_template('finish.html', score=percentage)
