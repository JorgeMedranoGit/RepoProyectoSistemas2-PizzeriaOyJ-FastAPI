from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ViewEncuesta(Base):
    __tablename__ = 'clustering_survey'
    __table_args__ = {'extend_existing': True}  # por si la vista ya existe

    id_cliente = Column(Integer, primary_key=True)
    satisfaction_1 = Column(Integer)
    satisfaction_2 = Column(Integer)
    satisfaction_3 = Column(Integer)
    satisfaction_4 = Column(Integer)
    satisfaction_5 = Column(Integer)
    consumption_frequency = Column(Integer)
    delivery_exp_1 = Column(Integer)
    delivery_exp_2 = Column(Integer)
    delivery_exp_3 = Column(Integer)
    delivery_exp_4 = Column(Integer)
    delivery_exp_5 = Column(Integer)
    reason_to_choose = Column(Integer)
    try_new_products = Column(Integer)
    considered_changing = Column(Integer)
