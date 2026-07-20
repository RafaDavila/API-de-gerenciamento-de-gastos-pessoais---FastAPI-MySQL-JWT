from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.dependencies import get_current_user
from app.models import TransactionType

router = APIRouter(prefix="/transactions", tags=["Transações"])


def _get_owned_transaction(db: Session, tx_id: int, user_id: int) -> models.Transaction:
    tx = (
        db.query(models.Transaction)
        .filter(models.Transaction.id == tx_id, models.Transaction.user_id == user_id)
        .first()
    )
    if not tx:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    return tx


@router.post("/", response_model=schemas.TransactionOut, status_code=status.HTTP_201_CREATED)
def create_transaction(
    tx_in: schemas.TransactionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if tx_in.category_id:
        category = (
            db.query(models.Category)
            .filter(models.Category.id == tx_in.category_id, models.Category.user_id == current_user.id)
            .first()
        )
        if not category:
            raise HTTPException(status_code=404, detail="Categoria não encontrada")

    tx = models.Transaction(
        description=tx_in.description,
        amount=tx_in.amount,
        type=tx_in.type,
        date=tx_in.date or datetime.utcnow(),
        notes=tx_in.notes,
        category_id=tx_in.category_id,
        user_id=current_user.id,
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx


@router.get("/", response_model=list[schemas.TransactionOut])
def list_transactions(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
    type: Optional[TransactionType] = Query(default=None, description="expense ou income"),
    category_id: Optional[int] = Query(default=None),
    start_date: Optional[datetime] = Query(default=None),
    end_date: Optional[datetime] = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
):
    query = db.query(models.Transaction).filter(models.Transaction.user_id == current_user.id)

    if type:
        query = query.filter(models.Transaction.type == type)
    if category_id:
        query = query.filter(models.Transaction.category_id == category_id)
    if start_date:
        query = query.filter(models.Transaction.date >= start_date)
    if end_date:
        query = query.filter(models.Transaction.date <= end_date)

    return (
        query.order_by(models.Transaction.date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get("/summary", response_model=schemas.MonthlySummary)
def get_summary(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
    start_date: Optional[datetime] = Query(default=None),
    end_date: Optional[datetime] = Query(default=None),
):
    query = db.query(models.Transaction).filter(models.Transaction.user_id == current_user.id)
    if start_date:
        query = query.filter(models.Transaction.date >= start_date)
    if end_date:
        query = query.filter(models.Transaction.date <= end_date)

    transactions = query.all()

    total_income = sum(t.amount for t in transactions if t.type == TransactionType.income)
    total_expense = sum(t.amount for t in transactions if t.type == TransactionType.expense)

    by_category_map: dict[str, float] = {}
    for t in transactions:
        if t.type == TransactionType.expense:
            key = t.category.name if t.category else "Sem categoria"
            by_category_map[key] = by_category_map.get(key, 0) + t.amount

    by_category = [
        schemas.SummaryByCategory(category=name, total=total)
        for name, total in sorted(by_category_map.items(), key=lambda x: -x[1])
    ]

    return schemas.MonthlySummary(
        total_income=total_income,
        total_expense=total_expense,
        balance=total_income - total_expense,
        by_category=by_category,
    )


@router.get("/{tx_id}", response_model=schemas.TransactionOut)
def get_transaction(
    tx_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return _get_owned_transaction(db, tx_id, current_user.id)


@router.put("/{tx_id}", response_model=schemas.TransactionOut)
def update_transaction(
    tx_id: int,
    tx_in: schemas.TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    tx = _get_owned_transaction(db, tx_id, current_user.id)

    update_data = tx_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(tx, field, value)

    db.commit()
    db.refresh(tx)
    return tx


@router.delete("/{tx_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(
    tx_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    tx = _get_owned_transaction(db, tx_id, current_user.id)
    db.delete(tx)
    db.commit()
    return None
