from fastapi import HTTPException,APIRouter
from    routes.rasa_route.rasa_api import app as rasa_app
app=APIRouter()
app.include_router(rasa_app)