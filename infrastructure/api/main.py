from fastapi import FastAPI
from infrastructure.api.routes import router
from infrastructure.mqtt.client import setup_mqtt, start_mqtt, stop_mqtt
from infrastructure.api.routes import use_case

app = FastAPI(title="Predictive Edge Simulator")
app.include_router(router)

@app.on_event("startup")
async def startup():
    setup_mqtt(use_case)
    start_mqtt()

@app.on_event("shutdown")
async def shutdown():
    stop_mqtt()


