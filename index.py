import sensai
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        text = request.form.get("text")
        evaluation = sensai.sentiment_analysis(text)
        label = "Polarity: " + evaluation[0]["label"]
        if evaluation[0]["label"] == "POSITIVE":
            percent_positive="Positive: " + str(int(evaluation[0]["score"] * 100))
            percent_negative="Negative: " + str(int(100 - (evaluation[0]["score" * 100])))
        else:
            percent_negative="Negative: " + str(int(evaluation[0]["score"] * 100))
            percent_positive="Positive: " + str(int(100 - (evaluation[0]["score" * 100])))
        
        return render_template('demo.html', label=label, percent_positive=percent_positive, percent_negative=percent_negative)
    label = ""
    return render_template('demo.html')
