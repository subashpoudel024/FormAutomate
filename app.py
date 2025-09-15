from dotenv import load_dotenv
from langchain_core.messages import  SystemMessage , HumanMessage
from langchain_groq import ChatGroq

load_dotenv()
llm = ChatGroq(model='llama-3.3-70b-versatile')

def generate_code(fields):
    system_prompt = """
You are an expert HTML form generator. 

Task:
- I will give you a list of fields I need in a form. 
- Your task is to generate a **complete, minimal, valid HTML <form> code** that can be submitted to a backend.

Rules:
1. The <form> must include `action="/submit"` and `method="post"` so that data can be captured by a backend route. 
2. Each input field must have an associated <label> with the `for` attribute correctly linked to the input's `id`.
3. Use semantic HTML5 input types (text, email, number, date, password, etc.) according to the field type.
4. If there are dropdowns, checkboxes, or radio buttons, generate them correctly.
5. Include a submit button at the end.
6. **Do not include any extra text, explanations, comments, or decorations** — only return the HTML code.
7. Make sure the generated HTML can be directly rendered in a browser and submitted.

Input Example: "I want fields for name, email, and age."
    """
    messages = [SystemMessage(content=system_prompt), HumanMessage(content=f'''The required fields are: {fields}''')]
    response = llm.invoke(messages)
    return response.content

import re

def extract_form(code):
    match = re.search(r"(<form[\s\S]*?</form>)", code)
    if match:
        return match.group(1)
    else:
        return ""

def save_code(code):
    with open("templates/generated_form.html", "w", encoding="utf-8") as f:
        f.write(code)

# raw_code = generate_code()
# fixed_code = extract_form(raw_code)
# save_code(fixed_code)