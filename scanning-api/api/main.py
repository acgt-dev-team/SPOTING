from fastapi import FastAPI
from api.controllers import agent

app = FastAPI()

app.include_router(agent.router)