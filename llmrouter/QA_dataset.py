import pandas as pd
import phoenix as px
from workflow_rng import run_rng_app
from workflow_llm import run_llm_app

#load data from csv into a dataframe
df = pd.read_csv('../data/data.csv')

#iterate over each row in dataframe, run predicton on the 'query' nd collect result with reference labels
#using either rng workflow or llm
results = []
prediction_mode = input('choose prediction mode (llm/rng): ')

for _, row in df.iterrows():
    if prediction_mode.lower() == 'llm':
        predict = run_llm_app(row['query'])
    elif prediction_mode.lower() == 'rng':
        predict = run_rng_app(row['query'])
    else:
        raise ValueError('Wrong mode.Type "llm" or "rng"')
    
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
        dataset_name=input('RNG-route1000'),
        input_keys=["query"],
        output_keys=["output"],
        metadata_keys=['reference']
    )