from pydantic import BaseModel
from typing import Optional, Dict, List, Union

class DocumentoEntrada(BaseModel):
    nombre_colleccion: str
    documentos: Optional[List[Dict]] = None

class DocumentoUpdate(BaseModel):
    nombre_colleccion: str
    actualizaciones: List[Dict]  # Cada dict debe incluir "_id" y los campos a actualizar

class DocumentoDelete(BaseModel):
    nombre_colleccion: str
    ids: List[str]  # lista de _id (como strings)