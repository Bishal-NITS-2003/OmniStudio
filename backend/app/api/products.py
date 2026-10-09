import uuid
import shutil
from pathlib import Path
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.config import settings
from app.models.product import Product
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductImportRequest,
    ProductImportResponse
)
from app.services.product_importer import extract_product_from_url

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).order_by(Product.id.desc()).all()

@router.post("", response_model=ProductResponse)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**payload.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, payload: ProductUpdate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    update_data = payload.dict(exclude_unset=True)
    for field, val in update_data.items():
        setattr(product, field, val)
    
    db.commit()
    db.refresh(product)
    return product

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}

@router.post("/import-url", response_model=ProductImportResponse)
def import_product_from_url(payload: ProductImportRequest):
    """
    Extracts product specifications from Amazon, Flipkart, or shopping URL.
    Returns preview for user verification before saving into inventory.
    """
    if not payload.url.startswith("http"):
        raise HTTPException(status_code=400, detail="Invalid URL format. Must start with http or https.")
    extracted = extract_product_from_url(payload.url)
    return extracted

@router.post("/upload-image")
def upload_product_image(file: UploadFile = File(...)):
    """Upload product photograph to local media storage."""
    file_ext = Path(file.filename).suffix or ".jpg"
    unique_name = f"upload_{uuid.uuid4().hex[:12]}{file_ext}"
    dest_path = settings.STORAGE_DIR / "uploads" / unique_name
    
    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return {
        "filename": unique_name,
        "url": f"/api/static/uploads/{unique_name}"
    }
