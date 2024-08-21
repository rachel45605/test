from flask import Flask, render_template, request
import google.generativeai as palm
import os

api = AIzaSyDtgxpFE0405T7m7l4llYVzW-eCb_Z-XMg
if not api:
    raise EnvironmentError("MAKERSUITE_API_TOKEN environment variable is not set")

palm.configure(api_key=api)
model = {"model": "models/chat-bison-001"}

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/genAI", methods=["GET", "POST"])
def getAI():
    q = request.form.get("q")
    if not q:
        return render_template("genAI.html", r="No input provided.")
    try:
        r = palm.chat(messages=q, **model)
        return render_template("genAI.html", r=r.last if hasattr(r, 'last') else "No response available.")
    except Exception as e:
        print(f"Error: {str(e)}")  # You can also use logging
        return render_template("genAI.html", r=f"Error: {str(e)}")

@app.route("/DApp", methods=["GET", "POST"])
def DApp():
    return render_template("DApp.html")

if __name__ == "__main__":
    app.run(debug=True)
