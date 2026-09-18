from fastapi import FastAPI

app = FastAPI(title="MikroTik Hotspot API")

@app.get("/")
def read_root():
    return {"message": "Hotspot Backend Çalışıyor!", "status": "success"}