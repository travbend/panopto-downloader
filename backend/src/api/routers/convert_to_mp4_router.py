from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from uuid import UUID, uuid4
from api.worker import worker, get_result
import os
from pathlib import Path
import aiofiles
from urllib.parse import urlparse
from sqlalchemy import select
from sqlalchemy.orm import Session
from common.data.sqlalchemy.engine import session_maker
from common.data.sqlalchemy.models.convert_to_mp4 import ConvertMp4Task
from common.constants.convert_to_mp4 import PENDING

router = APIRouter(
    prefix="/convert-to-mp4",
    tags=["convert-to-mp4"],
    responses={404: {"description": "Not found"}},
)

class InitiateRequest(BaseModel):
    video_url: str
    file_name: str

def is_valid_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
        return all([parsed.scheme, parsed.netloc])
    except ValueError:
        return False
    
def is_valid_unix_filename(filename: str) -> bool:
    return '/' not in filename and filename != '' and len(filename) <= 255

@router.post("/initiate")
async def initiate(params: InitiateRequest):
    if not is_valid_url(params.video_url):
        raise HTTPException(status_code=400, detail="Invalid video_url") 
    
    if not is_valid_unix_filename(params.file_name):
        raise HTTPException(status_code=400, detail="Invalid file_name") 
    
    task_id = uuid4()
    
    with session_maker() as session:
        row = ConvertMp4Task()
        row.key = task_id
        row.status = PENDING
        session.add(row)
        session.commit()
    
    worker.send_task('convert_to_mp4.convert', args=[params.video_url, params.file_name], task_id=str(task_id))
    return { "task_id": task_id }

def get_task_row(session: Session, task_id: UUID):
    statement = select(ConvertMp4Task).filter_by(key=task_id)
    task = session.scalar(statement)
    session.commit()
    return task

@router.get("/status/{task_id}")
async def status(task_id: UUID):
    with session_maker() as session:
        task = get_task_row(session, task_id)
        
        if task == None:
            raise HTTPException(status_code=404, detail="Task not found")
        
        return {
            "status": task.status,
            "is_cleaned": task.is_cleaned
        }

@router.get("/result/{task_id}")
async def result(task_id: UUID, background_tasks: BackgroundTasks):
    with session_maker() as session:
        task = get_task_row(session, task_id)
            
        if task == None:
            raise HTTPException(status_code=404, detail="Task not found")
        
        if task.is_cleaned:
            raise HTTPException(status_code=400, detail="Task result has been cleaned up")
    
    result = get_result(task_id)

    if result.state != "SUCCESS":
        raise HTTPException(status_code=400, detail="Task must be successful to download result file")
    
    file_path = result.get()
    file_name = os.path.basename(file_path)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404)

    background_tasks.add_task(delete_file, file_path)

    async def file_generator():
        async with aiofiles.open(file_path, mode="rb") as file:
            while chunk := await file.read(1024 * 1024):  # 1MB chunks
                yield chunk

    return StreamingResponse(file_generator(), media_type="application/octet-stream", headers={
        "Content-Disposition": "attachment; filename={}".format(file_name)
    })

def delete_file(file_path):
    if os.path.exists(file_path):
        Path.unlink(file_path)
        Path.rmdir(os.path.dirname(file_path))