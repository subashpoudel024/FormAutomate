from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from .utils.state import State
from .utils.nodes import FormGeneratorNode, CSSGeneratorNode, CombinerNode

class FormCreatorAgent:
    def __init__(self):
        self.memory = MemorySaver()

    def form_creator_graph(self):
        graph_builder= StateGraph(State)
        graph_builder.add_node("form_generator", FormGeneratorNode().run)
        graph_builder.add_node("css_generator", CSSGeneratorNode().run)
        graph_builder.add_node("combiner", CombinerNode().run)

        
        graph_builder.add_edge(START, "form_generator")
        graph_builder.add_edge("form_generator", 'css_generator')
        graph_builder.add_edge("css_generator", 'combiner')
        graph_builder.add_edge("combiner", END)

        return graph_builder.compile(checkpointer=self.memory)