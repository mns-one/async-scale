from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect

from . import service
from .ws_manager import hub
from .model import SimPayload

from ..simulation.state import State
from ..simulation.sim_utils import stop_sim_task

router = APIRouter(
    prefix = '/app-feature',
    tags=['app_feature']
)


@router.post("/data")
async def get_data(payload: SimPayload):
    
    if(State.is_started):
        raise HTTPException(
                status_code=400,
                detail="Another simulation going on, try again later..."
        )

    if not hub.is_connected(payload.client_id):
        raise HTTPException(
                    status_code=400,
                    detail="User not connected to server..."
    )
    
    await service.process_data(payload)
    return 

@router.websocket("/connect/{client_id}")
async def stream_socket(ws: WebSocket, client_id: str):
    await hub.connect(client_id, ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        print("Disconnecting client {client_id}...")
    except Exception as e:
        print(f"Websocket error for {client_id}: {e}")
    finally:
        await stop_sim_task();
        hub.disconnect(client_id)
