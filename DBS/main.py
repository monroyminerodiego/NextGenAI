# ===== Configuracion de API
from fastapi import FastAPI, APIRouter
app = FastAPI()
api_router = APIRouter()

# ===== Configuracion de Endpoints
from scripts.endpoints import prueba, collections
api_router.include_router(prueba.router)
api_router.include_router(collections.router)

app.include_router(api_router, prefix='/api-db')



