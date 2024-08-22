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

from flask import Flask, render_template, request
import requests
import os

# import google.generativeai as palm
# import os
# import openai

# api = ""
# palm.configure(api_key=api)
# model = {"model": "models/chat-bison-001"}

# os.environ["OPENAI_API_KEY"] = ""
# client = openai.OpenAI()

# Initialize Flask app
app = Flask(__name__)

# Get the API key from environment variables
api_key = os.getenv("MAKERSUITE_API_TOKEN")

# Define the correct Gemini API endpoint and headers
GEMINI_API_URL = "https://api.gemini.com/v1/generate"  # Replace with the actual endpoint
HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_key}'
}

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/ai_agent", methods=["GET","POST"])
def ai_agent():
    return(render_template("ai_agent.html"))

# @app.route("/genAI", methods=["GET","POST"])
# def genAI():
#     q = request.form.get("q")
#     r = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[{"role": "user", "content": q}],
#     )
#     r = r.choices[0].message.content
#     return(render_template("ai_agent_reply.html",r=r))


@app.route("/genAI", methods=["GET", "POST"])
def getAI():
    q = request.form.get("q")
    if not q:
        return render_template("genAI.html", r="No input provided.")
    
    try:
        # Prepare the request data for Gemini API
        data = {
            "prompt": q
        }

        # Make the API request
        response = requests.post(GEMINI_API_URL, headers=HEADERS, json=data, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Extract the generated text from the response
        result = response.json().get('text', 'No response from API.')
        return render_template("genAI.html", r=result)
    
    except requests.exceptions.RequestException as e:
        # Log and handle errors
        error_msg = f"An error occurred: {str(e)}"
        return render_template("genAI.html", r=error_msg)

@app.route("/prediction", methods=["GET","POST"])
def prediction():
    return(render_template("index.html"))

@app.route("/newRoute", methods=["POST"])
def newRoute():
    return "You have clicked the new button!"

if __name__ == "__main__":
    app.run(debug=True)
