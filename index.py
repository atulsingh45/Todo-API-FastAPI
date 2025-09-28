from fastapi import FastAPI


app = FastAPI()


@app.get("/ping")
def delete_todo():
    return {"ping": "pong"}