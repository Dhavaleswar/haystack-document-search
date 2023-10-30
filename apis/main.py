from fastapi import FastAPI
from fastapi.responses import JSONResponse

from apis.routes.server import ravis_apis


app = FastAPI()


@app.get("/")
def read_root():
    return JSONResponse(content={"message": "Hello, I'm Dhavaleswar"}, status_code=200)

app.include_router(ravis_apis, prefix="/ravis")