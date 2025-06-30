from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from ..schemas.collections_query import QueryVectorial
from ..vectorizer import embed_text
from ..vector_db import get_vector_collection

router = APIRouter()

class EndpointCollectionsQuery:

    @staticmethod
    @router.post("/collections/query")
    async def buscar_por_vector(data: QueryVectorial):
        try:
            collection = get_vector_collection(data.nombre_colleccion)
            vector = embed_text(data.consulta)

            resultados = collection.query(
                query_embeddings = [vector],
                n_results        = data.k,
                include          = ['documents', 'metadatas']
            )

            return JSONResponse(
                status_code = 201,
                content = {
                    "status": "ok",
                    "query": data.consulta,
                    "resultados": resultados
                }
            )

        except Exception as ex:
            raise HTTPException(
                status_code=500,
                detail={"status": "error", "mensaje": str(ex)}
            )