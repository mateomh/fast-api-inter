from fastapi import FastAPI

app = FastAPI()

@app.get('/health-check')
def root_path():
  return { "status": "ok" }