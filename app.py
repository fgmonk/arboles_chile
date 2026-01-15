from flask import Flask, render_template
from data import trees

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', trees=trees)

if __name__ == '__main__':
    app.run(debug=True)
