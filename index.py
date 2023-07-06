import sensai
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        text = request.form.get("text")
        evalution = sensai.sentiment_analysis(text)
        label = "Polarity: " + evalution[0]["label"]
        return render_template('demo.html', label=label)
    label = ""
    return render_template('demo.html')
