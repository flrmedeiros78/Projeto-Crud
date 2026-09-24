from pydantic import BaseModel, EmailStr, Field
from enum import Enum
from decimal import Decimal
from datetime import datetime
from typing import Annotated, Optional 

# Decimal maior que zero, reutilizável nos schemas
Valor = Annotated[Decimal, Field(gt=0, examples=[150.00])]

# producBase será o dem=nominador de todos os ostros(insert, delete e update)
class productBase(BaseModel): 
  name: str
  descricao: str
  valor: Valor
  categoria: str
  email_fornecedor: EmailStr
    

#herda os campos do productBase
class ProductCreate(productBase):
    pass

class ProductResponse(productBase):
  id: int
  dt_procs: datetime
  class Config:
    from_atributes = True

class ProductDelete():
    id: int 

class ProductUpdate(BaseModel):
  name: Optional [str] = None
  descricao: Optional [str] = None
  valor: Optional [Valor] = None     # Decimal > 0] = None
  categoria: Optional [str] = None
  email_fornecedor: Optional [EmailStr] = None
  