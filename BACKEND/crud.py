from itertools import product

from sqlalchemy.orm import Session
from schema import ProductUpdate, ProductCreate
from models import produtcModel

# função do modulo crud é responsável por definir as funções do CRUD utilizando SqlAlchemy ORM.

# SELECT * FROM tb_produtos
def get_products(db: Session):
  """Retorna todos os produtos"""
  return db.query(produtcModel).all() 

# SELECT * FROM tb_produtos WHERE id = 1
def get_product(db: Session, product_id:int):
  """Retorna somente um produto (ou None se não existir)"""
  return db.query(produtcModel).filter(produtcModel.id == product_id).first()

# INSERT
def create_product(db: Session, product: ProductCreate):
  # transforma minha view para ORM
  # usa do schema do pydantic e salva no schema do ORM
  # desempacotando com **product
  db_product = produtcModel(**product.model_dump())
  # so consigo usar o model.dump() pois no schema (class Config: from_atributes = True)
    
  db.add(db_product)     # adiciona na sessão
  db.commit()            # grava na tabela
  db.refresh(db_product) # recarrega do banco (traz id e dt_procs)
  return db_product      # retornar pro usuário o item criado
  
# DELETE WHERE id = 1
def delete_product(db: Session, product_id:int):
  # db_product =  db.query(produtcModel).filter(produtcModel.id == product_id).first()
  db_product = get_product(db, product_id)
  
  if db_product is None:
    return None
  
  db.delete(db_product)
  db.commit()
  return db_product
  
# UPDATE WHERE id = 1
def update_product(db: Session, product_id: int, product: ProductUpdate):
  #db_product =  db.query(produtcModel).filter(produtcModel.id == product_id).first()
  db_product = get_product(db, product_id)
   
  # exclude_unset=True: só traz os campos que o cliente realmente enviou
  # dados = product.model_dump(exclude_unset=True)
  # for k, v in dados.items():
  #   setattr(db_product, k, v)
  
  if db_product is None:
    return None
  
  if product.name is not None:
   db_product.name = product.name
  
  if product.descricao is not None:
   db_product.descricao = product.descricao
  
  if product.valor is not None:
   db_product.valor = product.valor
   
  if product.categoria is not None:
   db_product.categoria = product.categoria
  
  if product.email_fornecedor is not None:
    db_product.email_fornecedor = product.email_fornecedor
  
  db.commit()
  db.refresh(db_product)
  return db_product

  
    
    
