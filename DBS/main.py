# ===== Configuracion de API
from fastapi import FastAPI, APIRouter
app = FastAPI()
api_router = APIRouter()

# ===== Configuracion de Endpoints
from scripts.endpoints import prueba
from scripts.endpoints import collections
from scripts.endpoints import collections_query

api_router.include_router(prueba.router)            # /api-db/prueba 
api_router.include_router(collections.router)       # /api-db/collections
api_router.include_router(collections_query.router) # /api-db/collections/query

app.include_router(api_router, prefix='/api-db')



