from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from fastapi import Query
from fastapi.responses import JSONResponse
from app.services.clustering import generate_kmeans_plot
from app.services.clustering import generate_cluster_mean_plot
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.dependency import get_db
from sqlalchemy.orm import Session
from sklearn.cluster import KMeans
import pandas as pd
from sqlalchemy import text
router = APIRouter()


@router.get("/kmeans-image/cluster", response_class=StreamingResponse)
async def get_cluster_image(
    num: int = Query(..., ge=0, description="Número del clúster (ej. 0, 1, 2)"),
    db: Session = Depends(get_db)
):
    try:
        image_stream = generate_cluster_mean_plot(db, cluster_num=num)
        return StreamingResponse(image_stream, media_type="image/png")
    except ValueError as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

@router.get("/kmeans-image", response_class=StreamingResponse)
async def get_kmeans_image(db: Session = Depends(get_db)):
    image_stream = generate_kmeans_plot(db)
    return StreamingResponse(image_stream, media_type="image/png")

def fetch_view_data(db: Session):
    # Cambia 'your_view_name' por el nombre real de tu vista
    query = db.execute(text("SELECT * FROM clustering_survey"))
    rows = query.fetchall()
    columns = query.keys()
    df = pd.DataFrame(rows, columns=columns)
    return df

@router.get("/kmeans-temp")
async def kmeans_temp(db: Session = Depends(get_db)):
    df = fetch_view_data(db)

    # Convertir DataFrame a lista de diccionarios (json serializable)
    data_json = df.to_dict(orient="records")

    return JSONResponse(content=data_json)

@router.get("/decision-tree-image", response_class=StreamingResponse)
async def get_decision_tree_image(
    max_depth: int = Query(4, ge=1, le=10, description="Profundidad máxima del árbol"),
    db: Session = Depends(get_db)
):
    try:
        image_stream = generate_decision_tree_plot(db, max_depth=max_depth)
        return StreamingResponse(image_stream, media_type="image/png")
    except ValueError as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

