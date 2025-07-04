from random import randint
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

#Define our state wer using between nodes
class State(TypedDict):
    query: str
    message_type: str
    topic: str

#node for message classifying
def classify_message(state: State):
    query = randint(1, 5)
    if query == 1:
        return {'message_type': 'application'}
    elif query == 2:
        return {'message_type': 'entrance_exams'}
    elif query == 3:
        return {'message_type': 'syllabus_courses'}
    elif query == 4:
        return {'message_type': 'internship'}
    return {'message_type': 'other'}

#decides next node in the workflow based on the message type
def router(state: State):
    message_type = state.get('message_type')
    if message_type == 'application':
        return {'next': 'application'}
    elif message_type == 'entrance_exams':
        return {'next': 'entrance_exams'}
    elif message_type == 'syllabus_courses':
        return {'next': 'syllabus_courses'}
    elif message_type == 'internship':
        return {'next': 'internship'}
    return {'next': 'other'}

#each function represents a node in the workflow graph
def application(state: State):
    return {'topic': '1'} 

def entrance_exams(state: State):
    return {'topic': '2'}

def syllabus_courses(state: State):
    return {'topic': '3'}

def internship(state: State):
    return {'topic': '4'}

def other(state: State):
    return {'topic': '5'}

node_functions = {
    'application': application,
    'entrance_exams': entrance_exams,
    'syllabus_courses': syllabus_courses,
    'internship': internship,
    'other': other
}

#add all nodes to the workflow graph
workflow = StateGraph(State)
workflow.add_node('rng_classifier',classify_message)
workflow.add_node('router',router)

for node_name in node_functions:
    workflow.add_node(node_name,node_functions[node_name])

#building workflow graph with conditional routing
workflow.add_edge(START, 'rng_classifier')
workflow.add_edge('rng_classifier','router')
workflow.add_conditional_edges(
    'router',
    lambda state: state.get('next'),
    {
        'application': 'application','entrance_exams': 'entrance_exams',
        'syllabus_courses': 'syllabus_courses','internship': 'internship','other': 'other'
    }
)
for node_name in node_functions:
    workflow.add_edge(node_name, END)

app = workflow.compile()

#run compiled workflow graph on a user query and returns the topic
def run_rng_app(query):
    state = {'query': query}
    result = app.invoke(state)
    return result['topic']

#visualize and save state graph as png
with open("../assets/graph_rng.png", "wb") as f:
    f.write(app.get_graph(xray=True).draw_mermaid_png())
print('graph saved')