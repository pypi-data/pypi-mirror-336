import json

import tornado.httpclient
import tornado.websocket  
import os
import httpx
import jwt
from typing import AsyncGenerator
import asyncio

def generate_jwt_token(is_platform: bool) -> str:
    return jwt.encode(
        {"user_id": "test_user", "session_id": "test_session"},
        (
            os.environ["PLATFORM_JWT_SECRET_KEY"]
            if is_platform
            else os.environ["PORTAL_JWT_SECRET_KEY"]
        ),
        algorithm="HS512",
    )

def create_ws_request():
    return tornado.httpclient.HTTPRequest(
        "ws://localhost:8000/ws",
        headers={"Authorization": f"Bearer {generate_jwt_token(False)}"},
        validate_cert=False,
    )

async def receive_ws_msg(ws, parent_msg: str) -> AsyncGenerator[dict, None]:
    while True:
        msg = await ws.read_message()
        if msg is None:
            print("ws closed by server")
            break
        msg = json.loads(msg)
        if msg["msg_type"] == "end":
            break
        elif msg["msg_type"] == "response":
            print(msg["msg_content"])
        yield msg
    return


async def test_chat():
    
    ws_request = create_ws_request()
    ws = await tornado.websocket.websocket_connect(ws_request)
    ws_lock = asyncio.Lock()
    chat_msg = {
        "msg_type": "text",
        "msg_content": "chat",
        "kwargs": {"message_type": "text", "message_content": "How do you know this?"},
        "tokens": {"session_id": "test"},
        "msg_id": "01",
    }
    await ws.write_message(json.dumps(chat_msg))
    async with ws_lock:
        async for msg in receive_ws_msg(ws, "chat"):
            pass


if __name__ == "__main__":
    asyncio.run(test_chat())

