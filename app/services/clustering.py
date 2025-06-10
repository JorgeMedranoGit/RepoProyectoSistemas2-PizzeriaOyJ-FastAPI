import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from io import BytesIO
from sqlalchemy.orm import Session
from app.db.models.ViewEncuesta import ViewEncuesta
COLUMNS = [
    'satisfaction_1', 'satisfaction_2', 'satisfaction_3', 'satisfaction_4', 'satisfaction_5',
    'consumption_frequency',
    'delivery_exp_1', 'delivery_exp_2', 'delivery_exp_3', 'delivery_exp_4', 'delivery_exp_5',
    'reason_to_choose',
    'try_new_products',
    'considered_changing'
]

def fetch_survey_data(db: Session):
    # Recuperar todos los registros de la vista
    resultados = db.query(ViewEncuesta).all()

    # Convertir a DataFrame
    data = [{col: getattr(row, col) for col in COLUMNS} for row in resultados]
    return pd.DataFrame(data, columns=COLUMNS)
import matplotlib.pyplot as plt
from io import BytesIO

def generate_cluster_mean_plot(db: Session, cluster_num: int, n_clusters=3):
    df = fetch_survey_data(db)
    if df.empty:
        raise ValueError("No hay datos para analizar.")
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(df)
    df['cluster'] = labels

    if cluster_num not in df['cluster'].unique():
        raise ValueError(f"El clúster {cluster_num} no existe en los datos.")

    cluster_df = df[df['cluster'] == cluster_num].drop(columns=["cluster"])
    cluster_means = cluster_df.mean()

    plt.figure(figsize=(12, 6))
    cluster_means.plot(kind='bar', color='skyblue')
    plt.title(f'Promedios de respuestas - Clúster {cluster_num}')
    plt.ylabel('Valor promedio')
    plt.xlabel('Pregunta')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    return buffer

def generate_kmeans_plot(db: Session, n_clusters=3):
    df = fetch_survey_data(db)
    if df.empty:
        raise ValueError("No hay datos suficientes para generar el gráfico.")

    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(df)

    pca = PCA(n_components=2, random_state=42)
    reduced_data = pca.fit_transform(df)

    centers_df = pd.DataFrame(kmeans.cluster_centers_, columns=df.columns)
    centers_pca = pca.transform(centers_df)

    plt.figure(figsize=(8, 6))
    plt.scatter(reduced_data[:, 0], reduced_data[:, 1], c=labels, cmap='viridis', s=100, alpha=0.7)
    plt.scatter(centers_pca[:, 0], centers_pca[:, 1], c='red', s=200, marker='X', label='Cluster Centers')
    plt.title('K-means Encuesta General')
    plt.xlabel('PCA component 1')
    plt.ylabel('PCA component 2')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    return buffer
