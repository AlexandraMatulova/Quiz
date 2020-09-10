from flask import Flask, url_for, request
from flask import render_template
import random
from random import randint
import string
import sqlite3


app = Flask(__name__)
app.config['DEBUG'] = True 
print(app.root_path)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# SQLite execution
def sql_execute(sql):
    connection = sqlite3.connect('db.db')
    cursor = connection.cursor()
    ret = cursor.execute(sql)
    connection.commit()
    #connection.close()
    return ret

# Home page
@app.route('/')
def index():
    session_id = get_random_string(32)
    sql_execute(f"""
        INSERT INTO USERS (SESSION_ID, NO_CORRECT_ANSWERS)
        VALUES ('{session_id}', 0)
    """)
    return render_template('quiz_main.html', session_id=session_id)


# Question page
@app.route('/question_page', methods=["GET", "POST"])
def lets_start():
    session_id = request.form['session_id']

    # selecting question - excluding already asked questions
    cursor_answered_questions = sql_execute(f"""
        SELECT INDEX_ANSWERED_QUESTION FROM LIST_ANSWERED_QUESTIONS WHERE SESSION_ID = '{session_id}'
    """)
    answered_questions = cursor_answered_questions.fetchall()
    answered_questions_res = [item for t in answered_questions for item in t]
    question_index = randint(0, len(set_of_questions)-1)
    while question_index in answered_questions_res:
        question_index = randint(0, len(set_of_questions)-1)   
        if len(answered_questions_res) == 3:
            return render_template('quiz_result_page.html')
    question = set_of_questions[question_index]
    sql_execute(f"""
        INSERT INTO LIST_ANSWERED_QUESTIONS (SESSION_ID, INDEX_ANSWERED_QUESTION)
        VALUES ('{session_id}', {question_index})
    """)
    return render_template('quiz.html', question=question, question_index=question_index, session_id=session_id)


# Answer evaluation page
@app.route('/check_answer', methods=["GET", "POST"])
def check_answer():
    users_choice = request.form['Options']
    question_index = int(request.form['question_index'])
    question = set_of_questions[question_index]
    session_id = request.form['session_id']
    if users_choice == question['correct_answer']:
        cursor_no_correct_answers = sql_execute(f"""
            SELECT NO_CORRECT_ANSWERS FROM USERS WHERE SESSION_ID='{session_id}'
        """)
        no_correct_answers = cursor_no_correct_answers.fetchone()[0]
        no_correct_answers += 1
        sql_execute(f"""
            UPDATE USERS SET NO_CORRECT_ANSWERS={no_correct_answers} WHERE SESSION_ID='{session_id}'
        """)
    return render_template('quiz_evaluated_answer.html', users_choice=users_choice, question=question, session_id=session_id)


# List of questions
set_of_questions = [
    {
        "image": "images/allium_harry-grout-67I-shlEBLY-unsplash.jpg", 
        "question": "This flower is a genus of monocotyledonous flowering plants that includes hundreds of species, including the cultivated onion, garlic, scallion, shallot, leek, and chives. The generic name is a Latin word for garlic.",
        "answers": ["Allium", "Rose", "Agapanthus"],
        "correct_answer": "Allium"
    },
    {
        "image": "images/clematis_dusan-smetana-haCOsgRt0vo-unsplash.jpg",
        "question": "Their garden hybrids have been popular among gardeners,[7] beginning with Clematis × jackmanii, a garden standby since 1862; more hybrid cultivars are being produced constantly. They are mainly of Chinese and Japanese origin. Most species are known as clematis in English, while some are also known as traveller's joy, a name invented for the sole British native, C. vitalba, by the herbalist John Gerard; virgin's bower for C. terniflora, C. virginiana, and C. viticella; old man's beard, applied to several with prominent seedheads; leather flower for those with fleshy petals; or vase vine for the North American Clematis viorna.",
        "answers": ["Hemerocallis", "Paeonia", "Clematis"],
        "correct_answer": "Clematis"
    },
    {
        "image": "images/hortensia_lucie-goncalves-RWcsCAKUMDA-unsplash.jpg",
        "question": "It is a genus of 70–75 species of flowering plants native to Asia and the Americas. By far the greatest species diversity is in eastern Asia, notably Korea, China, and Japan. Most are shrubs 1 to 3 meters tall, but some are small trees, and others lianas reaching up to 30 m (98 ft) by climbing up trees. They can be either deciduous or evergreen, though the widely cultivated temperate species are all deciduous",
        "answers": ["Hydrangea", "Lantana", "Kalmia"],
        "correct_answer": "Hydrangea"
    }
]    


# Session ID: Random string with the combination of lower and upper case, length 32
def get_random_string(length):
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


if __name__ == "__main__":
    app.run()