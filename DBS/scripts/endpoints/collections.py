from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Optional
from bson import ObjectId
from ..db import mongo_db
from ..schemas.collections import DocumentoEntrada, DocumentoUpdate, DocumentoDelete
from ..vectorizer import embed_text

router = APIRouter()

class EndpointCollecciones:

    @staticmethod
    @router.post("/collections")
    async def crear_coleccion(data: DocumentoEntrada):
        try:
            coleccion = mongo_db[data.nombre_colleccion]
            ids = []                

            # ===== Guardar documentos
            if data.documentos:
                insert_result = await coleccion.insert_many(data.documentos)
                for doc_id in insert_result.inserted_ids: ids.append(str(doc_id))

                # for i, doc in enumerate(data.documentos):
                #     texto = doc.get("contenido") or doc.get("texto")
                #     if texto:
                #         embedding = embed_text(texto)
                #         print(f"[{i+1}] Embedding generado para '{texto[:30]}...': {embedding[:5]}")

            # ===== Confirmación
            if len(ids) > 0:
                response = {
                    "status": "creado!",
                    "mensaje": f"{len(ids)} documentos insertados",
                    "ids": ids
                }
            else:
                response = {
                    "status": "nothing happened!",
                    "mensaje": f"No se encontró un 'documento' o 'documentos' para guardar en la collección"
                }
            
            return JSONResponse(
                status_code = 201,
                content     = response
            )
        # ===== Manejo de errores generales
        except Exception as ex:
            raise HTTPException(
                status_code=500,
                detail={"status": "error", "mensaje": str(ex)}
            )
                
    @staticmethod
    @router.get("/collections")
    async def obtener_coleccion(nombre: Optional[str] = Query(None, description="Nombre de la colección")):
        try:
            if nombre:
                # Si se especifica el nombre de la colección, devuelve sus documentos
                coleccion = mongo_db[nombre]
                documentos_raw = await coleccion.find().to_list(length=1000)

                # Convertir ObjectId a str en cada documento
                documentos = []
                for doc in documentos_raw:
                    doc["_id"] = str(doc["_id"])
                    documentos.append(doc)
                return {
                    "estatus":"fetched!",
                    "coleccion": nombre,
                    "documentos": documentos
                }
            else:
                # Si no se especifica, devuelve los nombres de todas las colecciones
                colecciones = await mongo_db.list_collection_names()
                return {
                    "estatus":"fetched!",
                    "colecciones_disponibles": colecciones
                }
        except Exception as ex:
            raise HTTPException(
                status_code = 500,
                detail      = {
                    "estatus":"error!",
                    "mensaje":str(ex)
                }
            )

    @staticmethod
    @router.put("/collections")
    async def editar_coleccion(data: DocumentoUpdate):
        try:
            coleccion = mongo_db[data.nombre_colleccion]
            actualizados = []

            for i, doc in enumerate(data.actualizaciones):
                if "_id" not in doc: continue

                str_id = doc["_id"]
                del doc["_id"]

                result = await coleccion.update_one(
                    {"_id": ObjectId(str_id)},
                    {"$set": doc}
                )

                if result.modified_count:
                    actualizados.append(str_id)

                    # Opcional: revectorizar si se modifica el campo relevante
                    # texto = doc.get("contenido") or doc.get("texto")
                    # if texto:
                    #     embedding = embed_text(texto)
                    #     print(f"[{i+1}] Embedding actualizado para '{texto[:30]}...': {embedding[:5]}")

            return {
                "status": "actualizado!",
                "mensaje": f"{len(actualizados)} documentos actualizados",
                "ids": actualizados
            }

        except Exception as ex:
            raise HTTPException(
                status_code=500,
                detail={
                    "status": "error",
                    "mensaje": str(ex)
                }
            )

    @staticmethod
    @router.delete("/collections")
    async def borrar_coleccion(data: DocumentoDelete):
        try:
            coleccion = mongo_db[data.nombre_colleccion]
            eliminados = []

            for str_id in data.ids:
                result = await coleccion.delete_one({"_id": ObjectId(str_id)})
                if result.deleted_count == 1:
                    eliminados.append(str_id)

                    # Opcional: si manejas embeddings en otra colección, podrías eliminarlos también
                    # await mongo_db["embeddings"].delete_one({"doc_id": str_id})

            return {
                "status": "eliminado!",
                "mensaje": f"{len(eliminados)} documentos eliminados",
                "ids": eliminados
            }

        except Exception as ex:
            raise HTTPException(
                status_code=500,
                detail={
                    "status": "error",
                    "mensaje": str(ex)
                }
            )