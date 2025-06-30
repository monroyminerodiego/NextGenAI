from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Optional
from bson import ObjectId
from ..db import mongo_db
from ..schemas.collections import DocumentoEntrada, DocumentoUpdate, DocumentoDelete
from ..vectorizer import embed_text
from ..vector_db import get_vector_collection

router = APIRouter()

class EndpointCollecciones:

    @staticmethod
    @router.post("/collections")
    async def crear_coleccion(data: DocumentoEntrada):
        try:
            coleccion = mongo_db[data.nombre_colleccion]
            ids = []

            # Obtener colección en la base vectorial (ChromaDB)
            vector_collection = get_vector_collection(data.nombre_colleccion)

            # ===== Guardar múltiples documentos
            if data.documentos:
                insert_result = await coleccion.insert_many(data.documentos)
                inserted_ids = insert_result.inserted_ids

                docs_a_vectorizar = []
                ids_a_vectorizar = []
                metas_a_vectorizar = []

                for i, doc in enumerate(data.documentos):
                    doc_id = str(inserted_ids[i])
                    ids.append(doc_id)

                    texto = doc.get("contenido") or doc.get("texto")
                    if texto:
                        docs_a_vectorizar.append(texto)
                        ids_a_vectorizar.append(doc_id)
                        metas_a_vectorizar.append({"mongo_id": doc_id})

                # Vectorización en batch
                if docs_a_vectorizar:
                    embeddings = [embed_text(t) for t in docs_a_vectorizar]
                    vector_collection.add(
                        ids=ids_a_vectorizar,
                        documents=docs_a_vectorizar,
                        metadatas=metas_a_vectorizar
                    )

            # ===== Confirmación
            if len(ids) > 0:
                response = {
                    "status": "creado!",
                    "mensaje": f"{len(ids)} documentos insertados y vectorizados",
                    "ids": ids
                }
            else:
                response = {
                    "status": "nothing happened!",
                    "mensaje": "No se encontró 'documentos' para guardar en la colección"
                }

            return JSONResponse(status_code=201, content=response)

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
            vector_collection = get_vector_collection(data.nombre_colleccion)
            actualizados = []

            for i, doc in enumerate(data.actualizaciones):
                if "_id" not in doc:
                    continue  # Saltar si no hay ID

                str_id = doc["_id"]
                del doc["_id"]

                # Actualizar en Mongo
                result = await coleccion.update_one(
                    {"_id": ObjectId(str_id)},
                    {"$set": doc}
                )

                if result.modified_count:
                    actualizados.append(str_id)

                    # Si el contenido cambió, revectorizar
                    texto = doc.get("contenido") or doc.get("texto")
                    if texto:
                        # 1. Eliminar vector viejo
                        vector_collection.delete(ids=[str_id])
                        
                        # 2. Generar nuevo embedding
                        embedding = embed_text(texto)
                        
                        # 3. Insertar nuevo embedding
                        vector_collection.add(
                            ids=[str_id],
                            documents=[texto],
                            metadatas=[{"mongo_id": str_id}]
                        )
                        print(f"[{i+1}] Embedding actualizado para '{texto[:30]}...'")

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
            vector_collection = get_vector_collection(data.nombre_colleccion)
            eliminados = []

            for str_id in data.ids:
                result = await coleccion.delete_one({"_id": ObjectId(str_id)})
                if result.deleted_count == 1:
                    eliminados.append(str_id)

                    # Eliminar también el vector
                    vector_collection.delete(ids=[str_id])
                    print(f"[DELETE] Embedding eliminado para ID {str_id}")

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