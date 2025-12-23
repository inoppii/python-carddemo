import json
from src.models.models import Transaction, Account, Customer
from src.batch.p_CBEXPORT import export_table_to_csv # 既存を再利用 or 拡張

def unload_to_jsonl(table_class, file_path: str, db: Session = None):
    own_session = False
    if db is None:
        db = SessionLocal()
        own_session = True
    
    try:
        results = db.query(table_class).all()
        columns = [column.name for column in table_class.__table__.columns]
        
        with open(file_path, 'w', encoding='utf-8') as f:
            for row in results:
                data = {col: getattr(row, col) for col in columns}
                # datetime などのシリアライズ対応
                for k, v in data.items():
                    if isinstance(v, datetime):
                        data[k] = v.isoformat()
                f.write(json.dumps(data, ensure_ascii=False) + '\n')
        return len(results)
    finally:
        if own_session:
            db.close()
