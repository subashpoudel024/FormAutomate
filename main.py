from flask import Flask, request, render_template, jsonify , render_template_string
import pandas as pd
from app import generate_code , extract_form , save_code
import os
app = Flask(__name__)

CSV_FILE = "form_submissions.csv"


@app.route("/")
def index():
    return render_template("ask_field.html")

@app.route("/generate_form", methods=["GET","POST"])
def generate_form():
    fields=request.form.to_dict()
    print('The fields are:', fields)
    print('The method is:', request.method)
    if request.method =='POST':
        raw_code = generate_code(fields)
        fixed_code = extract_form(raw_code)
        save_code(fixed_code)
        # return render_template("index.html")
        return render_template_string(
        '{% extends "index.html" %}{% block form_block %}' + fixed_code + '{% endblock %}'
    )
    else:
        return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    # Capture all form fields dynamically
    form_data = request.form.to_dict()
    print('form data:', form_data)

    # Save to CSV using pandas
    df = pd.DataFrame([form_data])
    if os.path.exists(CSV_FILE):
        df.to_csv(CSV_FILE, mode="a", index=False, header=False)
    else:
        df.to_csv(CSV_FILE, index=False)

    # Return JSON response
    return jsonify(form_data)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render sets PORT env variable
    app.run(host="0.0.0.0", port=port)

