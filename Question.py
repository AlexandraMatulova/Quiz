from utils import sql_execute
from flask import url_for


class Question:
    def __init__(self, question_id):
        self.question_id = question_id
        cursor_question = sql_execute(f"SELECT * FROM QUESTIONS WHERE ID = '{question_id}'")
        question = dict(cursor_question.fetchone())
        self.id = question['id']
        self.question = question['question']
        self.answer1 = question['answer1']
        self.answer2 = question['answer2']
        self.answer3 = question['answer3']
        self.answers = [question['answer1'], question['answer2'], question['answer3']]
        self.correct_answer = question['correct_answer']
        self.category = question['category']
        self.image = question['image']

    def image_url(self):
        return url_for('static', filename=f"images/{self.image}")
    
    def is_correct_answer(self, users_choice):
        return users_choice == self.correct_answer
