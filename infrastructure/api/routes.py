from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from infrastructure.ws.broadcaster import active_websockets
from infrastructure.database.sqlite_message_repository import SqliteMessageRepository
from application.use_cases.save_message_usecase import SaveMessageUseCase

router = APIRouter()
templates = Jinja2Templates(directory="templates")

repo = SqliteMessageRepository()
use_case = SaveMessageUseCase(repo)

@router.get("/", response_class=HTMLResponse)
async def exibir_painel(request: Request):
    eventos = repo.list_recent(limit=10)
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "alerta_servidor": None,
            "topico_atual": "maquina/01/temp",
            "eventos": eventos,
        },
    )

@router.get("/events", response_class=JSONResponse)
async def eventos_json(date: str = None):
    if date:
        eventos = repo.list_by_date(date, limit=200)
    else:
        eventos = repo.list_recent(limit=100)
    return JSONResponse(content={"eventos": eventos})

@router.websocket("/ws/events")
async def websocket_events(websocket: WebSocket):
    await websocket.accept()
    active_websockets.add(websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        active_websockets.discard(websocket)
