from fastapi import APIRouter

router = APIRouter()

class EndpointPrueba:

    @staticmethod
    @router.get("/prueba")
    def mostrar_prueba():
        return {
            "estatus":"fetched!",
            "mensaje":"Endpoint creado a modo de prueba para validar funcionamiento"
        }