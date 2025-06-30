from pydantic import BaseModel
from typing import Optional

class QueryVectorial(BaseModel):
    nombre_colleccion: str
    consulta: str
    k: Optional[int] = 5  # número de resultados a devolver