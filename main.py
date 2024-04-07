from fastapi import FastAPI, BackgroundTasks
import uvicorn
from model import clean_data, compute_rfm, interpret_clusters, load_data, perform_kmeans_clustering, score_rfm

app = FastAPI()

@app.get("/")
async def home():
    return {"message": "Welcome to the RFM Model API. Use /run-model to execute the model."}

@app.get("/run-model")
async def run_model():
    try:
        # Step 1: Load dataset
        path = 'dataset/Online Retail.xlsx'
        response = {"status": "success", "messages": ["Loading dataset..."]}
        data = load_data(path)

        # Step 2: Clean data
        response['messages'].append("Dataset loaded. Cleaning data...")
        cleaned_data = clean_data(data)

        # Step 3: Compute RFM
        response['messages'].append("Data cleaned. Computing RFM...")
        rfm = compute_rfm(cleaned_data)

        # Step 4: Score RFM
        response['messages'].append("RFM computed. Scoring RFM...")
        scored_rfm = score_rfm(rfm)

        # Step 5: Perform K-Means Clustering
        response['messages'].append("RFM scored. Running model...")
        clustered_rfm = perform_kmeans_clustering(scored_rfm)

        # Step 6: Interpret Clusters
        response['messages'].append("Model running complete. Interpreting clusters...")
        cluster_summary = interpret_clusters(clustered_rfm)

        # Step 7: Prepare final response
        result = cluster_summary.to_dict(orient='records')
        response['cluster_summary'] = result
        response['messages'].append("Process complete.")

        return response

    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="debug", reload=False)
