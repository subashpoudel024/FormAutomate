from src.utils.models_loader import llm
from .state import State
from .prompts import form_creator_prompt , css_creator_prompt
from .utils import extract_form , extract_css
from langchain_core.messages import SystemMessage , HumanMessage

class FormGeneratorNode:
    def __init__(self):
        self.llm = llm
    
    def run(self,state:State):
        print('length:', len(state['messages']))
        if len(state['messages'])>11:
            state["messages"] = state["messages"][-9:]
        messages = [SystemMessage(content=form_creator_prompt)]+state['messages']
        response = llm.invoke(messages)
        form_code=extract_form(response.content)
        return {
            "messages": [{"role": "assistant", "content": f'''The form code is: {form_code}'''}],
            "form_code": form_code,
        }

class CSSGeneratorNode:
    def __init__(self):
        self.llm = llm

    def run(self, state:State):
        messages = [SystemMessage(content=css_creator_prompt)]+state['messages']
        response = llm.invoke(messages)
        print('The css code is:', response.content)
        css_code=extract_css(response.content)
        return {
            "messages": [{"role": "assistant", "content": f'''The css code is: {css_code}'''}],
            "css_code": css_code,
        }

class CombinerNode:
    def run(self, state: dict):
        form_code = state['form_code']

        # Ensure submit button exists
        if "<input" not in form_code.lower() or "type=\"submit\"" not in form_code.lower():
            # Insert before closing </form>
            if "</form>" in form_code:
                form_code = form_code.replace(
                    "</form>", 
                    '  <input type="submit" value="Submit" class="submit-btn">\n</form>'
                )
            else:
                # If somehow no </form>, wrap everything in a form
                form_code = f"<form action='/submit' method='post'>\n{form_code}\n  <input type='submit' value='Submit' class='submit-btn'>\n</form>"
        

        css_code = state['css_code'] + """
        .submit-btn {
            background-color: #28a745;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
        }
        .submit-btn:hover {
            background-color: #218838;
        }
        """  
        whole_code = f"""<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Form Page</title>
        <style>
    {css_code}
        </style>
    </head>
    <body>
    {form_code}
    </body>
    </html>"""

        return {
            'whole_code': whole_code
        }

