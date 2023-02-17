from fastapi import FastAPI, Form
from starlette.middleware.cors import CORSMiddleware

import uvicorn
import logging

logger = logging.getLogger('uvicorn')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
)

@app.get("/health")
async def health():
    return {"text": "OK"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        reload=True,
        port=8080,
        debug=True,
    )
