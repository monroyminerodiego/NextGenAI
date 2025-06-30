from fastapi import APIRouter

from ..vector_db import get_vector_collection

router = APIRouter()

class EndpointPrueba:

    @staticmethod
    @router.get("/prueba")
    def mostrar_prueba():
        return {
            "estatus":"fetched!",
            "mensaje":"Endpoint creado a modo de prueba para validar funcionamiento"
        }
    
    @staticmethod
    @router.get("/prueba/vector-debug")
    async def ver_vectores():
        col = get_vector_collection("prueba")
        return col.get(include=["documents", "metadatas"])