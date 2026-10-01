from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import json

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Voice Phishing Detection Test</title>
    </head>
    <body>
        <h1>Voice Streaming Test</h1>
        <button onclick="startStreaming()">마이크 스트리밍 시작</button>
        <div id="logs"></div>
        <script>
            let ws;
            async function startStreaming() {
                ws = new WebSocket("ws://localhost:8000/ws/audio");
                ws.onopen = () => {
                    document.getElementById("logs").innerText = "연결 성공! 오디오 스트리밍 중...";
                    // 가상의 오디오 데이터 전송 테스트
                    setInterval(() => {
                        if (ws.readyState === WebSocket.OPEN) {
                            ws.send(JSON.stringify({ score: Math.random() }));
                        }
                    }, 1000);
                };
                ws.onmessage = (event) => {
                    console.log("Server response:", event.data);
                };
            }
        </script>
    </body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws/audio")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received audio packet: {data}")
            await websocket.send_text(f"Processed packet: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")