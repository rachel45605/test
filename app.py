from flask import Flask, render_template, request, redirect, url_for, session
import google.generativeai as palm

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        api_key = request.form.get("api_key")
        if api_key:
            session['api_key'] = api_key  # Store API key in session
            palm.configure(api_key=api_key)
            return redirect(url_for('getAI'))
    return render_template("index.html")

@app.route("/genAI", methods=["GET", "POST"])
def getAI():
    if 'api_key' not in session:
        return redirect(url_for('index'))  # Redirect to index if no API key is found

    if request.method == "POST":
        q = request.form.get("q")
        if not q:
            return render_template("genAI.html", r="No input provided.")
        try:
            r = palm.chat(messages=q, model="models/chat-bison-001")
            return render_template("genAI.html", r=r.last if hasattr(r, 'last') else "No response available.")
        except Exception as e:
            return render_template("genAI.html", r=f"Error: {str(e)}")

    return render_template("genAI.html", r="")

@app.route("/DApp", methods=["GET", "POST"])
def DApp():
    return render_template("DApp.html")

if __name__ == "__main__":
    app.run(debug=True)

