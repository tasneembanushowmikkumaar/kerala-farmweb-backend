from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .agents import disease_detection

# The main FastAPI application
app = FastAPI(
    title="Kerala Farm Web API",
    description="API for AI-powered farming assistance.",
    version="1.0.0"
)

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, you should restrict this to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routers from the different agents
# The prefix="/api" means that all routes in the disease_detection router
# will be available under the /api path.
# For example, /predict in the router becomes /api/predict.
app.include_router(disease_detection.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Kerala Farm Web API"}

