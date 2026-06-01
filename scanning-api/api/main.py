from fastapi import FastAPI
from api.controllers import agent, user
from db.model.tapak import Tapak

app = FastAPI()

app.include_router(agent.router)
app.include_router(user.router)