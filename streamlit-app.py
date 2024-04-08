import streamlit as st
import requests
import matplotlib.pyplot as plt

# Set the page configuration
st.set_page_config(page_title="RFM Model App", layout="wide")

st.title("RFM Model Dashboard")

# Endpoint URLs
FASTAPI_ENDPOINT_ELBOW = "http://0.0.0.0:8000/elbow-curve"
FASTAPI_ENDPOINT_RUN_MODEL = "http://0.0.0.0:8000//run-model"

# Function to plot the elbow curve
def plot_elbow_curve(inertia):
    plt.figure(figsize=(8, 4))
    plt.plot(range(2, 11), inertia, marker='o')
    plt.title('Elbow Method For Optimal k')
    plt.xlabel('Number of clusters')
    plt.ylabel('Inertia')
    st.pyplot(plt)

# Fetch and display elbow curve
st.write("Generating elbow curve...")
response_elbow = requests.get(FASTAPI_ENDPOINT_ELBOW)
if response_elbow.status_code == 200:
    elbow_data = response_elbow.json()
    plot_elbow_curve(elbow_data["inertia"])

# User input for number of clusters
k = st.slider("Select the number of clusters (k)", 2, 10, 4)

# Button to run the model with the selected number of clusters
if st.button(f"Run RFM Model with {k} Clusters"):
    with st.spinner(f'Running the model with {k} clusters...'):
        response_model = requests.post(FASTAPI_ENDPOINT_RUN_MODEL, json={"k": k})
        if response_model.status_code == 200:
            result = response_model.json()
            if result["status"] == "success":
                st.success("Model run successfully with {k} clusters!")
                st.write(result["cluster_summary"])
            else:
                st.error("An error occurred: " + result["message"])
        else:
            st.error("Failed to connect to the model server.")
