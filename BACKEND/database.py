import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# comunicação com banco de dados postgres

#DATABASE_URL = "postgresql://user:password@postgres/mydatabase"
DATABASE_URL = os.getenv(
  "DATABASE_URL",
  "postgresql+psycopg2://user:password@postgres:5432/mydatabase",
)
engine = create_engine(DATABASE_URL)

# comit automatico falso
# atualização automatica falsp
# bind indica que a sessão é da engine
## ajustes:
# automomit=False não exsites mais no SqlAlchemy -> (retirado)
# expire_on_commit falso: permite devolver o objeto depois do commit (ex.: no delete) -> (incçuído)
SessionLocal = sessionmaker(autoflush=False, expire_on_commit=False, bind=engine)

Base = declarative_base() # ORM

# função geradora: cria uma instancia do sessionloal
# yeld é tipo um return mas não morre ao finalizar e pode ser chamada o tempo todo.
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()
