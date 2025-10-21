import streamlit as st
import requests

st.title("📚 Semantic PDF Explorer")

# Upload Section
st.header("Upload a PDF")
uploaded_file = st.file_uploader("Choose a PDF", type="pdf")
if uploaded_file is not None:
    response = requests.post("http://localhost:8000/upload", files={"file": uploaded_file})
    if response.status_code == 200:
        st.success(response.json()["message"])
    else:
        st.error(f"Upload failed: {response.text}")

# List Available Documents
st.header("Available Documents")
list_response = requests.get("http://localhost:8000/list")
if list_response.status_code == 200:
    docs = list_response.json()["documents"]
    selected_docs = st.multiselect("Select documents to query", options=docs)
else:
    st.error("Failed to fetch documents")

# Ask a Question
st.header("Ask a Question")
question = st.text_input("Enter your question")
if st.button("Ask") and question and selected_docs:
    ask_response = requests.get("http://localhost:8000/ask", params={"q": question, "docs": selected_docs})
    if ask_response.status_code == 200:
        result = ask_response.json()
        st.subheader("Answer")
        st.write(result["answer"])
        st.subheader("Follow-up Suggestions")
        for follow_up in result["follow_ups"]:
            st.write(f"- {follow_up}")
    else:
        st.error("Failed to get answer")

# Build Knowledge Graph
st.header("Build Knowledge Graph")
graph_file = st.file_uploader("Upload PDF for graph", type="pdf", key="graph")
if graph_file is not None:
    graph_response = requests.post("http://localhost:8000/graph", files={"file": graph_file})
    if graph_response.status_code == 200:
        st.success(graph_response.json()["message"])
    else:
        st.error(f"Graph build failed: {graph_response.text}")
