import chromadb
from chromadb.config import Settings

# Nuevo cliente local sin configuración adicional
client = chromadb.Client(settings=Settings(
    anonymized_telemetry=False,  
    persist_directory="/app/chroma_db" 
))

def get_vector_collection(nombre: str):
    return client.get_or_create_collection(name=nombre)