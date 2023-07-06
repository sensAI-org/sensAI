import sensai
from flask import Flask, render_template, request
from waitress import serve

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        text = request.form.get("text")
        evaluation = sensai.sentiment_analysis(text)
        if evaluation[0]["label"] == "POSITIVE":
            percent_positive="Positive: " + str(int(evaluation[0]["score"] * 100)) + "%"
            percent_negative="Negative: " + str(int(100 - (evaluation[0]["score"] * 100))) + "%"
        else:
            percent_negative="Negative: " + str(int(evaluation[0]["score"] * 100)) + "%"
            percent_positive="Positive: " + str(int(100 - (int(evaluation[0]["score"] *100)))) + "%"
        
        return render_template('demo.html', percent_positive=percent_positive, percent_negative=percent_negative, text=request.form.get("text"))
    return render_template('demo.html')

serve(app, host="0.0.0.0", port=8080)
print("this is runnign")