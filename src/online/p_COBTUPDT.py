from fastapi import APIRouter
import subprocess

router = APIRouter(prefix="/batch-control", tags=["batch"])

@router.post("/trigger/{batch_name}")
def trigger_batch_job(batch_name: str):
    # 本来は Cloud Run Jobs や Workflows を呼び出すが、
    # ここでは便宜上サブプロセス呼び出しのスケルトンとする
    return {"status": "Job triggered", "job_id": batch_name, "timestamp": datetime.utcnow()}
