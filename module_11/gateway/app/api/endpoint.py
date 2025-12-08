from fastapi import APIRouter

router_gateway = APIRouter()

@router_gateway.get("/books")
async def books():
    return {"status": "ok"}
