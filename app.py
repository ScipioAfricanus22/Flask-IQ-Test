from flask import Flask, request, render_template, jsonify
import json
import os

app = Flask(__name__)

# File to store IQ history
HISTORY_FILE = "history.json"

# Load history if exists, otherwise create an empty list
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r") as f:
        iq_history = json.load(f)
else:
    iq_history = []

@app.route('/')
def homepage():
    return render_template('homepage.html')  # Set homepage.html as the front page

@app.route('/test')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    global iq_history

    try:
        # Get form data
        q1 = int(request.form.get("q1", 0))
        q2 = int(request.form.get("q2", 0))
        q3 = int(request.form.get("q3", 0))
        q4 = int(request.form.get("q4", 0))

        # Calculate IQ
        iq = ((q1 + q2 + q3 + q4) / 16 * 100) 
        iq = round(iq, 2)

        # Store in history
        iq_history.append(iq)

        # Save to JSON file
        with open(HISTORY_FILE, "w") as f:
            json.dump(iq_history, f)

        # Calculate mean IQ
        mean_iq = round(sum(iq_history) / len(iq_history), 2)

        return render_template('result.html', iq=iq, mean_iq=mean_iq, iq_history=iq_history)

    except Exception as e:
        return str(e)

@app.route('/history')
def history():
    global iq_history

    # Load history if file exists
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            iq_history = json.load(f)

    return render_template('history.html', iq_history=iq_history)

if __name__ == '__main__':
    app.run(debug=True)
