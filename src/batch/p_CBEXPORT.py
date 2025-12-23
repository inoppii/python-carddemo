import csv
from sqlalchemy.orm import Session
from src.models.models import Customer, Account, Transaction
from src.utils.db import SessionLocal

def export_table_to_csv(table_class, file_path: str, db: Session = None):
    own_session = False
    if db is None:
        db = SessionLocal()
        own_session = True
    
    try:
        results = db.query(table_class).all()
        if not results:
            return 0
            
        columns = [column.name for column in table_class.__table__.columns]
        
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()
            for row in results:
                writer.writerow({col: getattr(row, col) for col in columns})
        
        return len(results)
    finally:
        if own_session:
            db.close()

if __name__ == "__main__":
    # 汎用エクスポート例
    export_table_to_csv(Customer, "customers_export.csv")
