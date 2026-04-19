from fastapi import FastAPI
import json

app = FastAPI()

@app.post('/mula-imbasan')
def mula_imbasan():
    with open('scanned_data.json', 'r') as cbom:
        return json.load(cbom)