# 🤯LLM Router 
is a user query classification system that identifies the most relevant topic for each incoming request and routes it to the appropriate process.

*LLM Workflow* - makes predictions using large language model

*RNG Workflow* - predictions based on simple rng

**Installation and Setup**

Clone the repo:
git clone <repository-url>
cd LLMrouter

Install dependencies:
pyproject.toml -> dependencies

Create .env file based on .env.example and configure environment variables.

Make prediction on dataset:
python QA_dataset.py

To evaluate the router's performance:
python QA_evaluation.py

*(check if phoenix serve is running)*

**Additional info:**

prompts.py contains prompt templates for query classification and evaluation

workflow visualizations are in assets

to customize classification, modify prompt in prompts.py