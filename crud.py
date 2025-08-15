from sqlalchemy.orm import Session
import models, schemas

def get_products(db: Session):
    return db.query(models.Product).all()

def create_order(db: Session, user_id: str, order: schemas.OrderCreate):
    db_order = models.Order(user_id=user_id, product_id=order.product_id, quantity=order.quantity)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_user_orders(db: Session, user_id: str):
    return db.query(models.Order).filter(models.Order.user_id == user_id).all()
