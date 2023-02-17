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

@app.get("/.well-known/web-identity")
async def wellKnown():
    return {
        "provider_urls": ["http://localhost:8080/config.json"],
    }

#
# IdP 設定ファイル
#
@app.get("/config.json")
async def config():
    return {
        "accounts_endpoint": "/accounts",
        "client_metadata_endpoint": "/client_metadata",
        "id_assertion_endpoint": "/assertion",
        "branding": {
            "background_color": "green",
            "color": "0xFFEEAA",
            "icons": [{
                "url": "http://localhost:8080/icon.ico",
                "size": 25
            }]
        }
    }

#
# アカウントリストエンドポイント
#
@app.get("/accounts")
async def accounts():
    return {
        "accounts": [{
            "id": "1234",
            "given_name": "John",
            "name": "John Doe",
            "email": "john_doe@idp.example",
            "picture": "http://localhost:8080/profile/123",
            "approved_clients": ["123", "456", "789"],
        }, {
            "id": "5678",
            "given_name": "Johnny",
            "name": "Johnny",
            "email": "johnny@idp.example",
            "picture": "http://localhost:8080/profile/456",
            "approved_clients": ["abc", "def", "ghi"],
        }]
    }

#
# クライアントメタデータエンドポイント
#
@app.get("/client_metadata")
async def clientMetadata():
    return {
        "privacy_policy_url": "http://localhost:8080/privacy_policy.html",
        "terms_of_service_url": "http://localhost:8080/terms_of_service.html",
    }

#
# ID アサーションエンドポイント
#
@app.post("/assertion")
async def assertion():
    return {
        "token": "12345",
    }

@app.get("/profile/{id}")
async def profile(id):
    print("ID: {}".format(id))
    return {
        "id": id,
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        reload=True,
        port=8080,
    )
