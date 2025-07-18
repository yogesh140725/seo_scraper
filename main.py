# Import the FastAPI app from the app module
from app.main import app

# This allows Render to find the app when using: uvicorn main:app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000) 