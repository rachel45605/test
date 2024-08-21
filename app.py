# from flask import Flask, render_template, request, redirect, url_for, session
# import google.generativeai as palm

# app = Flask(__name__)
# app.secret_key = 'your_secret_key'  # Needed for session management

# @app.route("/", methods=["GET", "POST"])
# def index():
#     return render_template("index.html")

# @app.route("/genAI", methods=["POST"])
# def getAI():
#     api_key = request.form.get("api_key")
#     if not api_key:
#         return "API key is required.", 400

#     session['api_key'] = api_key
#     palm.configure(api_key=api_key)

#     q = request.form.get("q")
#     if not q:
#         return render_template("genAI.html", r="No input provided.")

#     try:
#         r = palm.chat(messages=q, model="models/text-bison")
#         print(f"API Response: {r}")
#         return render_template("genAI.html", r=r.last if hasattr(r, 'last') else "No response available.")
#     except Exception as e:
#         print(f"Error: {str(e)}")  # Detailed error logging
#         return render_template("genAI.html", r=f"Error: {str(e)}")


# @app.route("/DApp", methods=["POST"])
# def DApp():
#     return render_template("DApp.html")

# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, render_template, request, session
import requests
import json
import logging

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

logging.basicConfig(level=logging.DEBUG)  # Enable detailed logging

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/genAI", methods=["POST"])
def getAI():
    api_key = request.form.get("api_key")
    if not api_key:
        return "API key is required.", 400

    session['api_key'] = api_key  # Store API key in session

    q = request.form.get("q")
    if not q:
        return render_template("genAI.html", r="No input provided.")

    try:
        # Construct the API request
        url = "https://generativelanguage.googleapis.com/v1beta/models/chat-bison-001:generateText"
        headers = {'Content-Type': 'application/json'}
        data = {
            "prompt": {
                "text": q
            }
        }

        # Make the API request
        response = requests.post(url, headers=headers, json=data, params={'key': api_key}, timeout=10)

        response.raise_for_status()  # Raise an exception for bad status codes

        # Extract the generated text from the response
        generated_text = response.json().get('result', {}).get('text', 'No response from API.')
        return render_template("genAI.html", r=generated_text)

    except requests.exceptions.RequestException as e:
        # Log the error
        logging.error(f"Error during API request: {str(e)}")

        # Provide a user-friendly error message
        if isinstance(e, requests.exceptions.Timeout):
            error_msg = "Request timed out. Please try again later."
        elif isinstance(e, requests.exceptions.ConnectionError):
            error_msg = "Connection error. Please check your internet connection."
        elif isinstance(e, requests.exceptions.HTTPError):
            error_msg = f"API request failed with status code: {e.response.status_code}"
        else:
            error_msg = "An unexpected error occurred. Please try again later."

        return render_template("genAI.html", r=error_msg)

@app.route("/DApp", methods=["POST"])
def DApp():
    return render_template("DApp.html")

@app.route("/newRoute", methods=["POST"])
def newRoute():
    return "You have clicked the new button!"

if __name__ == "__main__":
    app.run(debug=True)
