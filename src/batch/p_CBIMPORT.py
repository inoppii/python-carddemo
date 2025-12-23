import csv
from datetime import datetime
import csv
from sqlalchemy import DateTime, Integer, Float

def import_csv_to_table(table_class, file_path: str, db: Session = None):
    own_session = False
    if db is None:
        db = SessionLocal()
        own_session = True
    
    # 型情報の取得
    type_map = {}
    for column in table_class.__table__.columns:
        type_map[column.name] = column.type

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                converted_row = {}
                for key, value in row.items():
                    if not value:
                        converted_row[key] = None
                        continue
                    
                    col_type = type_map.get(key)
                    if isinstance(col_type, DateTime):
                        # ISO 形式等の文字列を datetime に変換
                        try:
                            converted_row[key] = datetime.fromisoformat(value)
                        except ValueError:
                            # 形式が合わない場合はそのまま（または別のパーサー）
                            converted_row[key] = value
                    elif isinstance(col_type, Integer):
                        converted_row[key] = int(value)
                    elif isinstance(col_type, Float):
                        converted_row[key] = float(value)
                    else:
                        converted_row[key] = value
                
                obj = table_class(**converted_row)
                db.merge(obj)
                count += 1
            db.commit()
            return count
    except Exception as e:
        db.rollback()
        raise e
    finally:
        if own_session:
            db.close()
