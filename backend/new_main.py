from fastapi import FastAPI, Depends, Body, HTTPException
from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "mysql+pymysql://root:dk6969@localhost/recipes?charset=utf8mb4"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class RawRecipe(Base):
    __tablename__ = "raw_recipes"
    id      = Column(Integer, primary_key=True, autoincrement=True)
    payload = Column(JSON, nullable=False)       # JSON column to store the entire raw JSON

# Create the table
Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.post("/recipe")
async def create_recipe(
    raw_payload: dict = Body(...),   # accept any JSON object
    db: Session    = Depends(get_db)
):
    """
    Stores the entire JSON request body into the `payload` JSON column.
    """
    try:
        db_obj = RawRecipe(payload=raw_payload)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
    except Exception as e:
        # Rollback on error & bubble up something user-friendly
        db.rollback()
        raise HTTPException(500, detail=f"DB error: {e!s}")

    return {
        "msg": "Recipe stored successfully",
        "id": db_obj.id
    }

@app.get("/")
async def root():
    return {"message": "Hello World"}