import pandas as pd
import phoenix as px
from workflow_rng import run_rng_app

#load data from csv into a dataframe
df = pd.read_csv('../data/data.csv')

#iterate over each row in dataframe, run predicton on the 'query' nd collect result with reference labels
#using either rng workflow or llm
results = []

for _, row in df.iterrows():
    predict = run_rng_app(row['query'])
    results.append({
        'query': row['query'],
        'output': predict,
        'reference': str(row['topic'])
    })

#creating dataset from prediction results
dataset_df = pd.DataFrame(results)

#initialize phoenix client and upload dataset for monitoring
phoenix_client = px.Client(endpoint="http://127.0.0.1:6006")

dataset = phoenix_client.upload_dataset(
        dataframe=dataset_df,
        dataset_name="LLM-route1000",
        input_keys=["query"],
        output_keys=["output"],
        metadata_keys=['reference']
    )