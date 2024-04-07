import pandas as pd
from sklearn.cluster import KMeans
import openpyxl

def load_data(path):
    print("Loading dataset...")
    data = pd.read_excel(path)
    print("Loading done!")
    return data

def clean_data(data):
    data.dropna(subset=['CustomerID'], inplace=True)
    data = data[(data['Quantity'] > 0) & (data['UnitPrice'] > 0)]
    data['CustomerID'] = data['CustomerID'].astype(int)
    return data

def compute_rfm(data):
    snapshot_date = max(data['InvoiceDate']) + pd.DateOffset(days=1)
    data['Total'] = data['Quantity'] * data['UnitPrice']
    rfm = data.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
        'InvoiceNo': 'nunique',
        'Total': 'sum'
    })
    rfm.rename(columns={'InvoiceDate': 'Recency', 'InvoiceNo': 'Frequency', 'Total': 'MonetaryValue'}, inplace=True)
    return rfm

def score_rfm(rfm):
    recency_bins = [rfm['Recency'].min()-1, 20, 50, 150, 250, rfm['Recency'].max()]
    frequency_bins = [rfm['Frequency'].min() - 1, 2, 3, 10, 100, rfm['Frequency'].max()]
    monetary_bins = [rfm['MonetaryValue'].min() - 3, 300, 600, 2000, 5000, rfm['MonetaryValue'].max()]
    rfm['R_Score'] = 5 - pd.cut(rfm['Recency'], bins=recency_bins, labels=range(1, 6), include_lowest=True).astype(int) + 1
    rfm['F_Score'] = pd.cut(rfm['Frequency'], bins=frequency_bins, labels=range(1, 6), include_lowest=True).astype(int)
    rfm['M_Score'] = pd.cut(rfm['MonetaryValue'], bins=monetary_bins, labels=range(1, 6), include_lowest=True).astype(int)
    return rfm

def perform_kmeans_clustering(rfm):
    X = rfm[['R_Score', 'F_Score', 'M_Score']]
    inertia = []
    for k in range(2, 11):
        kmeans = KMeans(n_clusters=k, n_init=10, random_state=42)
        kmeans.fit(X)
        inertia.append(kmeans.inertia_)
    print("Inertia for k [Elbow method]:", inertia)
    n_clusters = 4
    print("Running k-means with k =", n_clusters)
    best_kmeans = KMeans(n_clusters, n_init=10, random_state=42)
    rfm['Cluster'] = best_kmeans.fit_predict(X)
    return rfm

def interpret_clusters(rfm):
    cluster_summary = rfm.groupby('Cluster').agg({
        'R_Score': 'mean',
        'F_Score': 'mean',
        'M_Score': 'mean'
    }).reset_index()
    print("Model running complete!")
    return cluster_summary

def main():
    path = 'dataset/Online Retail.xlsx'
    data = load_data(path)
    cleaned_data = clean_data(data)
    rfm = compute_rfm(cleaned_data)
    scored_rfm = score_rfm(rfm)
    clustered_rfm = perform_kmeans_clustering(scored_rfm)
    cluster_summary = interpret_clusters(clustered_rfm)

    # Print the main output
    print("\n", cluster_summary)

if __name__ == "__main__":
    main()
