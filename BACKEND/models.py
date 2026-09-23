# responsabilidade do arquivo model.py é fazer o modelo do database;

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from  database import Base

# class productModel é uma representação da tabela
class produtcModel(Base):
    __tablename__ = "tb_produtos" # Nome da tabela
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    descricao = Column(String)
    valor = Column(float)
    categoria = Column(String)
    email_fornecedor = Column(String)
    dt_procs = Column(DateTime(timezone=True), dafault=func.now())
    