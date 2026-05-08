import asyncio
from fastapi import APIRouter, HTTPException, Request, WebSocket, WebSocketDisconnect
from . import service
from .ws_manager import hub

router = APIRouter(
    prefix = '/app-feature',
    tags=['app_feature']
)

IS_STARTED = False

@router.get("/data")
async def get_data(client_id: str, size: int):
    global IS_STARTED

    if not size:
        raise HTTPException(
            status_code=400,
            detail="Size cant be empty"
        )
    
    if(IS_STARTED):
        raise HTTPException(
                status_code=400,
                detail="Another simulation going on, try again later..."
        )

    if not hub.is_connected(client_id):
        raise HTTPException(
                    status_code=400,
                    detail="User not connected to server..."
    )
    
    IS_STARTED = True
    await service.process_data(size)
    return 

@router.websocket("/connect/{client_id}")
async def stream_socket(ws: WebSocket, client_id: str):
    await hub.connect(client_id, ws)
    try:
        while True:
            await asyncio.sleep(3600)
    except WebSocketDisconnect:
        hub.disconnect(client_id)
    except Exception:
        hub.disconnect(client_id)