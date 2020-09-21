import pytest
import http.client
import random
import string
from question import Question

def test_load_question():
    question = Question(0)
    assert question.answer1 == 'Allium'
    assert question.answer2 == 'Rose'
    assert question.answer3 == 'Agapanthus'
    assert question.correct_answer == 'Allium'
    assert question.category == 'Flowers'
    assert question.image == 'allium_harry-grout-67I-shlEBLY-unsplash.jpg'

def test_correct_answer():
    question = Question(0)
    users_choice = question.answer1
    assert users_choice == question.correct_answer

def test_incorrect_answer():
    question = Question(0)
    users_choice = question.answer2
    assert users_choice != question.correct_answer

def random_string_length():
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    assert len(result_str) == 32

# source: https://docs.python.org/3/library/http.client.html
def test_home_page():
    conn = http.client.HTTPConnection('127.0.0.1:5000')
    conn.request('GET', '/')
    response = conn.getresponse()
    assert response.status == 200