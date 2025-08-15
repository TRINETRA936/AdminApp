from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine, Base
from firebase_auth import verify_firebase_token

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Auth Dependency
async def get_current_user(authorization: str = Header(...)):
    token = authorization.split(" ")[1] if " " in authorization else authorization
    user_info = await verify_firebase_token(token)
    if not user_info:
        raise HTTPException(status_code=401, detail="Invalid Firebase token")
    return user_info

# Routes
@app.get("/products", response_model=list[schemas.ProductOut])
def list_products(db: Session = Depends(get_db)):
    return crud.get_products(db)

@app.post("/orders", response_model=schemas.OrderOut)
async def place_order(order: schemas.OrderCreate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.create_order(db, user_id=user["localId"], order=order)

@app.get("/orders", response_model=list[schemas.OrderOut])
async def get_orders(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.get_user_orders(db, user_id=user["localId"])
