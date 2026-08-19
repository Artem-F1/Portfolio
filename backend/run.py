import uvicorn
import os

if __name__ == "__main__":
    reload = os.getenv("ENV", "development") == "development"
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=reload
    )
