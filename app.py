from flask import Flask, render_template, url_for, request, redirect
import os
from twitter_api import inp

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        keywordR = str(request.form['keyword'])
        if len(keywordR) > 0:
            kw = inp(keywordR)
            os.system('python sentiment_model.py')
            return render_template('result.html', keyword=keywordR)
        else:
            return redirect(url_for('home'))
    return redirect(url_for('home'))

# test
def get_k():
    f_keyword = 'dear'
    return f_keyword

if __name__ == "__main__":
    app.run(debug=True)