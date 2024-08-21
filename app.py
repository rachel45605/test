from flask import Flask, render_template, request, redirect, url_for, session
import google.generativeai as palm

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/genAI", methods=["POST"])
def getAI():
    api_key = request.form.get("api_key")
    if not api_key:
        return "API key is required.", 400

    session['api_key'] = api_key
    palm.configure(api_key=api_key)

    q = request.form.get("q")
    if not q:
        return render_template("genAI.html", r="No input provided.")

    try:
        r = palm.chat(messages=q, model="models/chat-bison-001")
        print(f"API Response: {r}")
        return render_template("genAI.html", r=r.last if hasattr(r, 'last') else "No response available.")
    except Exception as e:
        print(f"Error: {str(e)}")  # Detailed error logging
        return render_template("genAI.html", r=f"Error: {str(e)}")


@app.route("/DApp", methods=["POST"])
def DApp():
    return render_template("DApp.html")

if __name__ == "__main__":
    app.run(debug=True)

