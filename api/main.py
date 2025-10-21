from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import papers

app = FastAPI()

# Allow requests from Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your Streamlit domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include all routes from papers.py (no trailing slash!)
app.include_router(papers.router, prefix="")

# ✅ Preload services after startup
@app.on_event("startup")
async def preload_services():
    papers.initialize_services()
