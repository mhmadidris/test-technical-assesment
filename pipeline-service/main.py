from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
import models.customer as models
from database import get_db, engine, Base
from services.ingestion import run_ingestion

app = FastAPI(title="Pipeline Service")

@app.on_event("startup")
async def startup():
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/api/ingest")
async def ingest_data():
    try:
        records_processed = await run_ingestion()
        return {"status": "success", "records_processed": records_processed}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/customers")
async def get_customers(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    offset = (page - 1) * limit
    
    # Get total count
    count_query = select(func.count()).select_from(models.Customer)
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # Get data
    query = select(models.Customer).offset(offset).limit(limit)
    result = await db.execute(query)
    customers = result.scalars().all()
    
    return {
        "data": customers,
        "total": total,
        "page": page,
        "limit": limit
    }

@app.get("/api/customers/{customer_id}")
async def get_customer(customer_id: str, db: AsyncSession = Depends(get_db)):
    query = select(models.Customer).filter(models.Customer.customer_id == customer_id)
    result = await db.execute(query)
    customer = result.scalar_one_or_none()
    
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return customer
