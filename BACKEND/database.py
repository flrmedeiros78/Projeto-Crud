from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# comunicação com banco de dados postgres

#DATABASE_URL = "postgresql://user:password@postgres/mydatabase"
DATABASE_URL = "postgresql+psycopg2://user:password@postgres:5432/mydatabase"
engine = create_engine(DATABASE_URL)

# comit automatico falso
# atualização automatica falsp
# bind indica que a sessão é da engine
SessionLocal = sessionmaker(automomit=False, autoflush=False, bind=engine)

Base = declarative_base() # ORM

# função geradora: cria uma instancia do sessionloal
# yeld é tipo um return mas não morre ao finalizar e pode ser chamada o tempo todo.
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()
