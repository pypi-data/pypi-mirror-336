from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse

from arq_base_python.entrypoints_base.command_receiver.src.commands.web.command_handler import CommandHandler

router = APIRouter()


@router.post("/commands")
async def command(request: Request):
    """
    Recibe un comando en formato JSON y lo procesa

    :return: _description_
    """
    var10001 = CommandHandler()

    try:
        data = await request.json()
    except Exception:
        data = None
    return await var10001.receive_command(request, data)


@router.get("/anon/health")
async def health_check():
    return PlainTextResponse("OK")
