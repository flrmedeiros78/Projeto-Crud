from pydantic import BaseModel, PositiveFloat, EmailStr, validators
from enum import Enum as en
from datetime import datetime as dt
from typing import Optional as opt

# producBase será o dem=nominador de todos os ostros(insert, delete e update)
class productBase(BaseModel): 
  name: str
  descricao: str
  valor: PositiveFloat
  categoria: str
  email_fornecedor: EmailStr
    

#herda os campos do productBase
class ProductCreate(productBase):
    pass

class ProductResponse(productBase):
  id: int
  dt_procs: dt # dt -> datetime
  class Config:
    from_atributes = True

class ProductDelete():
    id: int 

class ProductUpdate():
  name: opt [str] = None
  descricao: opt [str] = None
  valor: opt [PositiveFloat] = None
  categoria: opt [str] = None
  email_fornecedor: opt [EmailStr] = None
  
  


