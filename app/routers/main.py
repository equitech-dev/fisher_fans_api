from fastapi import APIRouter, Response
from fastapi.openapi.docs import get_swagger_ui_html
import os

router = APIRouter()
from fastapi.responses import JSONResponse

@router.get("/openapi.json", include_in_schema=False)
async def get_swagger_ui():
    return JSONResponse(content=get_swagger_ui_html(openapi_url="/openapi.json", title="Fisher Fans API").to_dict())
