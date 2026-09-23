from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session 
from database import SessionLocal, get_db
from schema import ProductCreate, ProductUpdate, ProductResponse
from typing import List
from crud import (
  get_products,
  create_product,
  delete_product,
  update_product
)

router = APIRouter()

# criar rota de buscar todos os itens
#Sempre vamos ter ter 2 atributos obrigatórios, o PATH e o RESPONSE
@router.get("/products/", response_model=list[ProductResponse])
def read_all_products(db: Session = Depends(get_db)):
  products = get_products(db)
  return products

# criar rota de buscar 1 item
@router.get("/products/{product_id}", response_model=ProductResponse)
def read_one_product(product_id: int, db: Session = Depends(get_db)):
  db_product = get_products(db=db, product_id=product_id)
  
  if db_product is None:
    raise HTTPException(status_code=404, detail="Produto não existe na base de dados!")  
  return db_product
    
# cria rota de adicionar um item
@router.post("/products/", response_model=ProductResponse)
def create_product(product:ProductCreate, db:Session = Depends(get_db)):
  return create_product(product=product, db=db)

# criar rota de deletar item
@router.delete("/products/{product_id}", response_model=ProductResponse)
def Delete_product(product_id: int, db: Session = Depends(get_db)):
  
  if product_db is None:
    raise HTTPException(status_code=404, detail="Produto não existe para ser deletado!")
  return product_db

# criar rota para fazer update nos itens
@router.url_path_for("/products/{product_id}", response_model=ProductResponse)
def atualizar_product(product_id: int, product: ProductUpdate, db: Session=Depends(get_db)):
  product_db = update_product(db=db, product_id=product_id, product=product)
  
  if product_db is None:
      raise HTTPException(status_code=404, detail="Produto não existe para ser Atualizado!")
  product_db