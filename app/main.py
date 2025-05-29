from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="K-Means Clustering API",
    description="Agrupa clientes y devuelve una imagen de los clusters.",
)

app.include_router(router)
