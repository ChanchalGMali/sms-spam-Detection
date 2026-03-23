from flask import Flask, request, render_template
import os

app = Flask(_name_)

@app.route('/')
def home():
    return "App is running"

if _name_ == "_main_":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)