from flask import Blueprint, render_template, request
import requests

client_bp = Blueprint('client', __name__, template_folder='templates')

@client_bp.route('/')
def vote_form():
    return render_template('vote_form.html')

@client_bp.route('client/submit_vote', methods=['POST'])
def submit_vote():
    voter_id = request.form['voter_id']
    candidate = request.form['candidate']

    payload = {
        'voter_id': voter_id,
        'candidate': candidate
    }

    try:
        # Change this to your deployed votingapi URL
        response = requests.post('http://127.0.0.1:5001/vote', json=payload)
        if response.status_code == 200:
            return f"<h3>Vote submitted successfully for {candidate}!</h3><a href='/client'>Vote Again</a>"
        else:
            return f"<h3>Error: {response.text}</h3><a href='/client'>Try Again</a>"
    except Exception as e:
        return f"<h3>Server error: {e}</h3>"
