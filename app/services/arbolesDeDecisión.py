import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, plot_tree
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
    resultados = db.query(ViewEncuesta).all()
    data = [{col: getattr(row, col) for col in COLUMNS} for row in resultados]
    return pd.DataFrame(data, columns=COLUMNS)

def generate_decision_tree_plot(db: Session, max_depth: int = 4):
    df = fetch_survey_data(db)
    if df.empty:
        raise ValueError("No hay datos para entrenar el árbol.")

    if 'considered_changing' not in df.columns:
        raise ValueError("Falta la columna 'considered_changing' como variable objetivo.")

    X = df.drop(columns=['considered_changing'])
    y = df['considered_changing']

    clf = DecisionTreeClassifier(criterion='entropy', max_depth=max_depth, random_state=42)
    clf.fit(X, y)

    plt.figure(figsize=(22, 12))
    plot_tree(clf, 
              feature_names=X.columns, 
              class_names=['No Cambiaría', 'Sí Cambiaría'], 
              filled=True, 
              rounded=True,
              fontsize=10)
    plt.title("Árbol de Decisión - Consideración de Cambio de Pizzería")
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    return buffer
