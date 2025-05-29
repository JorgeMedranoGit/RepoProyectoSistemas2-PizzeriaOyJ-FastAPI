from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from fastapi.responses import JSONResponse
from app.services.clustering import generate_kmeans_plot
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.dependency import get_db
from sqlalchemy.orm import Session
from sklearn.cluster import KMeans
import pandas as pd
from sqlalchemy import text
router = APIRouter()

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
