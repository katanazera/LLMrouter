import time
import prompts
import phoenix as px
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from phoenix.experiments.types import Example
from phoenix.experiments import run_experiment
from phoenix.experiments.evaluators import create_evaluator

load_dotenv()

#initialize phoenix client and retrieve named dataset
client = px.Client(endpoint="http://127.0.0.1:6006")
dataset = client.get_dataset(name="LLM-route1000")

#initialize our LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.1,
)

#create a prompt template set up output parser and chain them with llm
prompt = PromptTemplate.from_template(prompts.QA_PROMPT_TEMPLATE)
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

#takes example object and returns its output field as a dict
def get_output(example: Example) -> dict:
    return dict(example.output)

#evaluates accuracy of QA response using llm chain, returns 1 for correct answer and 0 otherwise
@create_evaluator(name="QA accuracy rate", kind="LLM")
def qa_evaluator(input: dict, output: dict, metadata: dict) -> int:
    verdict = chain.invoke({
        "input": input["query"],
        "reference": metadata["reference"],
        "output": output["output"]
    })
    time.sleep(2)
    return 1 if verdict.strip().lower() == "correct" else 0

#run an expirement to evaluate the dataset using qa_evaluator
run_experiment(
    dataset,
    get_output,
    evaluators=[qa_evaluator],
    experiment_name="QA_test"
)