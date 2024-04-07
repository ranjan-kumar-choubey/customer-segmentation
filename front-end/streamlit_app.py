import streamlit as st
import requests

# Set the page configuration
st.set_page_config(page_title="RFM Model App", layout="wide")

st.title("RFM Model Dashboard")

# URL of the FastAPI endpoint
FASTAPI_ENDPOINT = "http://localhost:8000/run-model"

# Button to run the model
if st.button("Run RFM Model"):
    with st.spinner('Running the model...'):
        response = requests.get(FASTAPI_ENDPOINT)
        if response.status_code == 200:
            result = response.json()
            if result["status"] == "success":
                st.success("Model run successfully!")
                st.write(result["cluster_summary"])
            else:
                st.error("An error occurred: " + result["message"])
        else:
            st.error("Failed to connect to the model server.")

st.write("Click the button above to run the RFM Model.")
