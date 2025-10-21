import streamlit as st
import requests

API_URL="http://localhost:8000"

  # 🔁 Replace with your actual deployed backend URL

st.set_page_config(page_title="Autonomous Research Agent", layout="wide")
st.title("📚 Autonomous Research Agent")
st.write("Upload research papers, ask questions, and explore knowledge graphs.")

# 📁 Upload PDF
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
if uploaded_file is not None:
    st.write("Uploading:", uploaded_file.name)
    files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
    try:
        res = requests.post(f"{API_URL}/upload", files=files)
        if res.status_code == 200:
            try:
                data = res.json()
                if "message" in data:
                    st.success(data["message"])
                elif "error" in data:
                    st.error(f"Upload failed: {data['error']}")
                else:
                    st.error("Upload succeeded but response format was unexpected.")
            except Exception as e:
                st.error(f"Upload succeeded but response was not JSON: {str(e)}")
        else:
            st.error(f"Upload failed with status code {res.status_code}")
    except requests.exceptions.ConnectionError:
        st.error("Backend not reachable. Make sure your FastAPI server is deployed and online.")

# 🔍 Ask a question
st.subheader("Ask a Question")
question = st.text_input("Enter your question")
docs = st.text_input("Document name(s)", value=uploaded_file.name if uploaded_file else "")

if st.button("Ask"):
    params = {"q": question, "docs": docs, "top_k": 5, "min_score": 0.1}
    try:
        res = requests.get(f"{API_URL}/ask", params=params)
        if res.status_code == 200:
            try:
                data = res.json()
                st.markdown(f"**Answer:** {data['answer']['answer']}")
                st.markdown(f"**Source:** {data['answer']['source'][:500]}...")
                st.markdown("**Follow‑up suggestions:**")
                for f in data["follow_ups"]:
                    st.write("-", f)
            except Exception as e:
                st.error(f"Answer received but response was not JSON: {str(e)}")
        else:
            st.error(f"Error fetching answer. Status code: {res.status_code}")
    except requests.exceptions.ConnectionError:
        st.error("Backend not reachable. Make sure your FastAPI server is deployed and online.")

# 🧠 Build Knowledge Graph
st.subheader("Build Knowledge Graph")
if st.button("Extract Graph"):
    params = {"docs": docs}
    try:
        res = requests.post(f"{API_URL}/graph", params=params)
        if res.status_code == 200:
            try:
                data = res.json()
                st.success(data["message"])
                st.json(data["triples_sample"])
            except Exception as e:
                st.error(f"Graph extracted but response was not JSON: {str(e)}")
        else:
            st.error(f"Graph extraction failed. Status code: {res.status_code}")
    except requests.exceptions.ConnectionError:
        st.error("Backend not reachable. Make sure your FastAPI server is deployed and online.")
