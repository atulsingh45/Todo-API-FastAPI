from fastapi import FastAPI


app = FastAPI()


@app.get("/ping")
def check_ping():
    return {"ping": "pong"}