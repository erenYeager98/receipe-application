from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, Dict
from sqlalchemy import create_engine, Table, Column, Integer, String, Float, MetaData, Text, JSON, select, desc, func, and_, or_
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.engine import Result
import re


# Database setup
DATABASE_URL = "mysql+pymysql://root:dk6969@localhost/recipes"
engine = create_engine(DATABASE_URL)
metadata = MetaData()

recipes = Table(
    "recipes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("cuisine", String(255)),
    Column("title", String(255)),
    Column("rating", Float),
    Column("prep_time", Integer),
    Column("cook_time", Integer),
    Column("total_time", Integer),
    Column("description", Text),
    Column("nutrients", JSON),
    Column("serves", String(255)),
)

metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Pydantic model
class Recipe(BaseModel):
    cuisine: str
    title: str
    rating: float
    prep_time: int
    cook_time: int
    total_time: int
    description: str
    nutrients: Dict
    serves: str

# FastAPI app
app = FastAPI()

@app.post("/add_recipe")
def add_recipe(recipe: Recipe):
    try:
        with engine.connect() as conn:
            conn.execute(recipes.insert().values(**recipe.dict()))
        return {"message": "Recipe added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/recipes")
def get_recipes(page: int = Query(1, gt=0), limit: int = Query(10, gt=0)):
    offset = (page - 1) * limit
    with engine.connect() as conn:
        total = conn.execute(select(func.count()).select_from(recipes)).scalar()
        statement = recipes.select().order_by(desc(recipes.c.rating)).offset(offset).limit(limit)
        result = conn.execute(statement)
        rows = [dict(row._mapping) for row in result]

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "data": rows
    }


@app.get("/api/recipes/search")
def search_recipes(
    title: Optional[str] = Query(None),
    cuisine: Optional[str] = Query(None),
    total_time: Optional[int] = Query(None),
    total_time_op: Optional[str] = Query("eq"), 
    rating: Optional[float] = Query(None),
    rating_op: Optional[str] = Query("eq"),    
    calories: Optional[int] = Query(None),
    calories_op: Optional[str] = Query("eq")    
):
    filters = []

    if title:
        filters.append(recipes.c.title.ilike(f"%{title}%"))
    if cuisine:
        filters.append(recipes.c.cuisine == cuisine)

    if total_time is not None:
        if total_time_op == "lt":
            filters.append(recipes.c.total_time < total_time)
        elif total_time_op == "gt":
            filters.append(recipes.c.total_time > total_time)
        else:
            filters.append(recipes.c.total_time == total_time)

    if rating is not None:
        if rating_op == "lt":
            filters.append(recipes.c.rating < rating)
        elif rating_op == "gt":
            filters.append(recipes.c.rating > rating)
        else:
            filters.append(recipes.c.rating == rating)

    if calories is not None:
        # Nutrients -> calories (stored as string like "389 kcal")
        if calories_op == "lt":
            filters.append(func.cast(func.json_extract(recipes.c.nutrients, "$.calories"), Integer) < calories)
        elif calories_op == "gt":
            filters.append(func.cast(func.json_extract(recipes.c.nutrients, "$.calories"), Integer) > calories)
        else:
            filters.append(func.cast(func.json_extract(recipes.c.nutrients, "$.calories"), Integer) == calories)

    with engine.connect() as conn:
        statement = select(recipes).where(and_(*filters))
        result = conn.execute(statement)
        rows = [dict(row._mapping) for row in result]

    return {"data": rows}
