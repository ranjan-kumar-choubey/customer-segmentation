import pandas as pd
from sklearn.cluster import KMeans
import joblib

# Load and preprocess your data
def load_data():
    path = 'dataset/Online Retail.xlsx'
    data = pd.read_excel(path)
    data.dropna(subset=['CustomerID'], inplace=True)
    data = data[(data['Quantity'] > 0) & (data['UnitPrice'] > 0)]
    data['CustomerID'] = data['CustomerID'].astype(int)
    data['Total'] = data['Quantity'] * data['UnitPrice']
    return data

def compute_rfm(data):
    snapshot_date = max(data['InvoiceDate']) + pd.DateOffset(days=1)
    rfm = data.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
        'InvoiceNo': 'nunique',
        'Total': 'sum'
    })
    rfm.rename(columns={'InvoiceDate': 'Recency', 'InvoiceNo': 'Frequency', 'Total': 'MonetaryValue'}, inplace=True)
    return rfm


def calculate_elbow_curve(data, max_k=10):
    rfm = compute_rfm(data)
    X = rfm[['Recency', 'Frequency', 'MonetaryValue']]
    inertia = []
    for k in range(1, max_k + 1):
        kmeans = KMeans(n_clusters=k, n_init=10, random_state=42)
        kmeans.fit(X)
        inertia.append(kmeans.inertia_)
    return {"k_values": list(range(1, max_k + 1)), "inertia": inertia}


data = load_data()
rfm = compute_rfm(data)

# Pre-compute K-means models for a range of k
for k in range(2, 11):  # Adjust range as needed
    X = rfm[['Recency', 'Frequency', 'MonetaryValue']]
    kmeans = KMeans(n_clusters=k, n_init=10, random_state=42)
    kmeans.fit(X)
    joblib.dump(kmeans, f'models/kmeans_k{k}.joblib')
