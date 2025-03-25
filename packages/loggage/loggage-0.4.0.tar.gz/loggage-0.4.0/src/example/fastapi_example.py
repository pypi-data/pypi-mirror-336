import asyncio

from fastapi import  FastAPI, Request
from fastapi.responses import JSONResponse

from src.core.decorators import operation_logger
from src.core.hybrid_logger import HybridOperationLogger
from src.utils.config import load_config

config = load_config("/home/zalex/PycharmProjects/loggage/config/config.yaml")
HybridOperationLogger().initialize(config)

app = FastAPI()


def get_request():
    return Request


@app.get("/api/users")
@operation_logger(resource_type="User", action="create",
                  obj_id="123", obj_name="user123",
                  ref_id="456", ref_name="456")
async def create_user(request: Request):
    return JSONResponse({"hello": "FastAPI"}, status_code=200)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app, host="0.0.0.0", port=8080)
