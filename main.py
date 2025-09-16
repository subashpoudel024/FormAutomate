from flask import Flask, request, render_template, jsonify , render_template_string
import pandas as pd
from src.form_creator_agent.agent import FormCreatorAgent
form_creator_agent = FormCreatorAgent()
creator_graph = form_creator_agent.form_creator_graph()

import os
app = Flask(__name__)

CSV_FILE = "form_submissions.csv"
config={"configurable": {"thread_id": "ai-form-thread"}}

@app.route("/", methods=["GET", "POST"])
def index():
    generated_code = None
    if request.method == "POST":
        query = request.form.to_dict()
        print("The fields are:", query)

        result = creator_graph.invoke(
            {"messages": query["fields"]},
            config=config
        )
        generated_code = result["whole_code"]
        form_code = result['form_code']
        print('Form code is:',form_code)

    return render_template("layout.html", generated_code=generated_code)


# @app.route("/generate_form", methods=["GET","POST"])
# def generate_form():
#     query=request.form.to_dict()
#     print('The fields are:', query)
#     print('The method is:', request.method)
#     if request.method =='POST':
#         result=creator_graph.invoke({
#             'messages':query['fields']
#         },config=config)
        
#         return render_template_string(result['whole_code'])
#     else:
#         return render_template("index.html")


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

# app.run(debug=True) 