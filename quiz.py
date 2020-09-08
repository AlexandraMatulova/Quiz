from flask import Flask, url_for, request
from flask import render_template
import random
from random import randint


app = Flask(__name__)
app.config['DEBUG'] = True 
print(app.root_path)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route('/')
def index():
    return render_template('quiz_main.html')

@app.route('/lets_start', methods=["GET", "POST"])
def lets_start():
    #question = random.choice(set_of_questions)
    question_index = randint(0, len(set_of_questions)-1)
    print(question_index)
    return render_template('quiz.html', question=set_of_questions[question_index])

@app.route('/check_answer', methods=["GET", "POST"])
def check_answer():
    users_choice = request.form['Options']
    return render_template('quiz_evaluated_answer.html', users_choice=users_choice, question=question)

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



if __name__ == "__main__":
    app.run()