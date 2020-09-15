from flask import Flask, url_for, request
from flask import render_template
import random
from random import randint
import string
from Question import Question
from utils import sql_execute

app = Flask(__name__)
app.config['DEBUG'] = True 
print(app.root_path)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


# Home page
# generates a home page with a form to select a category of questions
# after submitting the form the users is directed to 'question_page'
@app.route('/', methods=["GET", "POST"])
def index():
    # session_id to distinguish between users, the value is passed from page to page
    session_id = get_random_string(32)

    # insert of session_id and no_correct_answers into 'users' table
    sql_execute(f"INSERT INTO USERS (SESSION_ID, NO_CORRECT_ANSWERS) VALUES ('{session_id}', 0)")
    return render_template('quiz_home_page.html', session_id=session_id)


# Question page, redirect to Result page
@app.route('/question_page', methods=["GET", "POST"])
def lets_start():
    # gets session_id from previous request
    session_id = request.form['session_id']

    # gets selected category of questions from home page or database
    if 'category' in request.form:
        category = request.form['category'] 
        sql_execute(f"UPDATE USERS SET CATEGORY = '{category}' WHERE SESSION_ID = '{session_id}'")    
    else:
        cursor_category = sql_execute(f"SELECT CATEGORY FROM USERS WHERE SESSION_ID = '{session_id}'")
        category = cursor_category.fetchone()[0]

    # selects question - excludes already asked questions
    cursor_answered_questions = sql_execute(f"""
        SELECT INDEX_ANSWERED_QUESTION FROM LIST_ANSWERED_QUESTIONS WHERE SESSION_ID = '{session_id}'
    """)
    answered_questions = cursor_answered_questions.fetchall()
    answered_questions_res = [item for t in answered_questions for item in t]

    # gets list of IDs of questions from the chosen category
    cursor_question_ids = sql_execute(f"SELECT ID FROM QUESTIONS WHERE CATEGORY = '{category}'")
    question_ids = cursor_question_ids.fetchall()
    question_ids_res = [item for t in question_ids for item in t]

    #generates random question ID
    question_id = question_ids_res[randint(0, len(question_ids_res)-1)]
    while question_id in answered_questions_res:
        question_id = question_ids_res[randint(0, len(question_ids_res)-1)]

        #goes to result page when all questions of category answered
        if len(answered_questions_res) == len(question_ids_res):
            cursor_no_correct_answers = sql_execute(f"""
                SELECT NO_CORRECT_ANSWERS FROM USERS WHERE SESSION_ID = '{session_id}'
            """)
            no_correct_answers = cursor_no_correct_answers.fetchone()[0]
            no_questions = len(question_ids_res)
            return render_template('quiz_result_page.html', no_correct_answers=no_correct_answers, no_questions=no_questions)
    
    sql_execute(f"""
        INSERT INTO LIST_ANSWERED_QUESTIONS (SESSION_ID, INDEX_ANSWERED_QUESTION)
        VALUES ('{session_id}', {question_id})
    """)

    question = Question(question_id)
    return render_template('quiz_question_page.html', question=question, session_id=session_id)

# Answer evaluation page
@app.route('/check_answer', methods=["GET", "POST"])
def check_answer():
    users_choice = request.form['Options']
    session_id = request.form['session_id']
    question = Question(int(request.form['question_index']))

    # adds +1 to no of correct answeres in database
    if question.is_correct_answer(users_choice):
        cursor_no_correct_answers = sql_execute(f"""
            SELECT NO_CORRECT_ANSWERS FROM USERS WHERE SESSION_ID='{session_id}'
        """)
        no_correct_answers = cursor_no_correct_answers.fetchone()[0]
        no_correct_answers += 1
        sql_execute(f"""
            UPDATE USERS SET NO_CORRECT_ANSWERS={no_correct_answers} WHERE SESSION_ID='{session_id}'
        """)
    return render_template('quiz_evaluated_answer.html', users_choice=users_choice, question=question, session_id=session_id)


# Session ID: Random string with the combination of lower and upper case, length 32
def get_random_string(length):
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


if __name__ == "__main__":
    app.run()