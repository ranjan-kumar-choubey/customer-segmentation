from fastapi import FastAPI, HTTPException
import pandas as pd
import joblib

from model import calculate_elbow_curve, compute_rfm, load_data

app = FastAPI()
data = load_data()  # Load the data as in the previous script

# Function to use a pre-computed model for RFM analysis
def rfm_analysis_with_precomputed_model(data, k):
    try:
        kmeans = joblib.load(f'models/kmeans_k{k}.joblib')
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Model for k={k} not found")

    rfm = compute_rfm(data)
    X = rfm[['Recency', 'Frequency', 'MonetaryValue']]
    rfm['Cluster'] = kmeans.predict(X)
    
    return rfm.groupby('Cluster').mean().to_dict()



@app.get("/")
async def health_check():
    print("Home API hitted !! ")
    return {"message": "API is up and running"}


@app.get("/elbow-curve")
async def elbow_curve():
    print("Elbow Curve API hitted")
    return calculate_elbow_curve(data)



@app.post("/run-rfm")
async def run_rfm(k: int):
    print("run-rfm api hitted with k",k)
    if k <= 0:
        raise HTTPException(status_code=400, detail="k must be a positive integer")
    return rfm_analysis_with_precomputed_model(data, k)

# FastAPI main function and other endpoints
# ...

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
