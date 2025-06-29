from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, SessionLocal
from .auth import authenticate_user

# Create DB tables

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
@app.get("/")
async def root():
    return {"message": "Welcome to Grocery API folks!"}

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)

@app.get("/products/", response_model=list[schemas.Product])
def read_products(db: Session = Depends(get_db)):
    return crud.get_products(db)

@app.get("/protected")
async def protected_route(current_user: str = Depends(authenticate_user)):
    return {"message": f"Hello {current_user}, this is a protected route!"}
