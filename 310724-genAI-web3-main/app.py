from flask import Flask, render_template,request
import google.generativeai as palm
import os

api = os.getenv("MAKERSUITE_API_TOKEN")
palm.configure(api_key=api)
model = {"model": "models/chat-bison-001"}

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():
    return(render_template("index.html"))

@app.route("/genAI", methods=["GET","POST"])
def getAI():
    q = request.form.get("q")
    r = palm.chat(messages=q, **model)
    return(render_template("genAI.html",r=r.last))

@app.route("/DApp", methods=["GET","POST"])
def DApp():
    return(render_template("DApp.html"))

if __name__ == "__main__":
    app.run()
