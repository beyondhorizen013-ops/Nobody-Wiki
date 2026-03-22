from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

def get_github_data(username):
    url = f"https://api.github.com/users/{username}"
    # Note: For high traffic, you'd need a GitHub Token here
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/wiki/<username>')
def wiki(username):
    data = get_github_data(username)
    if not data:
        return "<h1>User not found.</h1><p>They are so obscure they don't even have a GitHub.</p>", 404
    
    # The Joke: If they are too famous, kick them out
    if data.get('followers', 0) > 500:
        return "<h1>Error: 403 Too Famous</h1><p>This encyclopedia is only for the non-notable. Please go to the real Wikipedia.</p>", 403

    return render_template('wiki.html', user=data)

if __name__ == '__main__':
    app.run(debug=True)
