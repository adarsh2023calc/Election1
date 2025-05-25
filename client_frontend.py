from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

# Show voting form
@app.route('/')
def vote_form():
    return render_template('vote_form.html')

# Handle form submission
@app.route('/submit_vote', methods=['POST'])
def submit_vote():
    voter_id = request.form['voter_id']
    candidate = request.form['candidate']

    # Send to vote API as JSON (like curl)
    payload = {
        'voter_id': voter_id,
        'candidate': candidate
    }

    try:
        response = requests.post('http://localhost:5001/vote', json=payload)
        if response.status_code == 200:
            return f"<h3>Vote submitted successfully for {candidate}!</h3><a href='/'>Vote Again</a>"
        else:
            return f"<h3>Error: {response.text}</h3><a href='/'>Try Again</a>"
    except Exception as e:
        return f"<h3>Server error: {e}</h3>"

if __name__ == '__main__':
    app.run(port=5003)
