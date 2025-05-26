from flask import Flask, render_template,Blueprint, request, redirect
import requests


client_bp = Blueprint('client', __name__)



# Show voting form
@client_bp.route('/')
def vote_form():
    return render_template('vote_form.html')

# Handle form submission
@client_bp.route('client/submit_vote', methods=['POST'])
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
            return f"<h3>Error: {response.text}</h3><a href='/client'>Try Again</a>"
    except Exception as e:
        return f"<h3>Server error: {e}</h3>"

if __name__ == '__main__':
    client_bp.run(port=5003)
