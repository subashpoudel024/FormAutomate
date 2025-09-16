from src.form_creator_agent.agent import FormCreatorAgent
form_creator_agent = FormCreatorAgent()
creator_graph = form_creator_agent.form_creator_graph()

config={"configurable": {"thread_id": "analytics-chatbot-thread"}}
result=creator_graph.invoke({
    'messages':'I want name and email fields in blue background and silver colour in the fields.'
},config=config)

print('Form Code:\n', result['form_code'])
print('CSS Code:\n', result['css_code'])
print('Whole Code:\n', result['whole_code'])

