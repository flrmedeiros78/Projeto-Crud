from itertools import product

from sqlalchemy.orm import Session
from schema import ProductUpdate, ProductCreate
from models import produtcModel

# função do modulo crud é responsável por definir as funções do CRUD utilizando SqlAlchemy ORM.

# get all (SELECT * FROM) -> função para pegar todos os produtos:

def get_products(db: Session):
  """" Essa função retorna todos os produtos"""
  return db.query(produtcModel).all() 

# get where id = 1 
def get_products(db: Session, product_id:int):
  """" Essa função retorna somente um produto"""
  return db.query(produtcModel).filter(produtcModel.id == product_id).first()

# insert int(create)
def create_product(db: Session, product: ProductCreate):
  # transforma minha view para ORM
  # usa do schema do pydantic e salva no schema do ORM
  # desempacotando com **product
  db_product = produtcModel(**product.model_dump())
  # so consigo usar o model.dump() pois no schema (class Config: from_atributes = True)
    
  # adicionar na tabela
  db.add(db_product)
  
  # commitar na tabela
  db.commit()
  
  # fazer o refrash do banco de dados
  db.refrash(db_product)
  
  # retornar pro usuário o item criado
  return db_product
  
# delete where id = 1
def delete_product(db: Session, product_id:int):
  db_product =  db.query(produtcModel).filter(produtcModel.id == product_id).first()
  db.delete(db_product)
  db.commit()
  return db_product
  
# update where id = 1

def update_product(db: Session, product_id: int, ProductUpdate):
  db_product =  db.query(produtcModel).filter(produtcModel.id == product_id).first()
  
  if db_product is None:
    return None
  
  if db_product.name is not None:
    db_product.name = product.name
  
  if db_product.descricao is not None:
    db_product.descricao = product.descricao
  
  if db_product.valor is not None:
    db_product = product.valor
  
  if db_product.categoria is not None:
    db_product = product.categoria
    
  if db_product.email_fornecedor is not None:
    db_product = product.email_fornecedor
  
  db.commit()
  return db_product

  
    
    
