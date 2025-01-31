from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from uuid import UUID, uuid4
from api.worker import worker, get_result
from urllib.parse import urlparse
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from common.data.sqlalchemy.engine import session_maker
from common.data.sqlalchemy.models.convert_to_mp4 import ConvertMp4Task
from common.constants.convert_to_mp4 import PENDING
from common.data.b2.engine import b2_bucket
from common.config import settings

router = APIRouter(
    prefix="/convert-to-mp4",
    tags=["convert-to-mp4"],
    responses={404: {"description": "Not found"}},
)

class InitiateRequest(BaseModel):
    video_url: Optional[str]
    file_name: Optional[str]

def is_valid_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
        return all([parsed.scheme, parsed.netloc])
    except ValueError:
        return False
    
def is_valid_unix_filename(filename: str) -> bool:
    return filename != None and '/' not in filename and filename != '' and len(filename) <= 255

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
async def result(task_id: UUID):
    with session_maker() as session:
        task = get_task_row(session, task_id)
            
        if task == None:
            raise HTTPException(status_code=404, detail="Task not found")
        
        if task.is_cleaned:
            raise HTTPException(status_code=400, detail="Task result has been cleaned up")
    
    result = get_result(task_id)

    if result.state != "SUCCESS":
        raise HTTPException(status_code=400, detail="Task must be successful to retrieve result")
    
    file_name = str(task_id) + '.mp4'
    authorization = b2_bucket.get_download_authorization(file_name, settings.b2_token_seconds)
    base_download_url = b2_bucket.get_download_url(file_name)
    download_url = f"{base_download_url}?Authorization={authorization}"
    return {
        "download_url": download_url
    }
    
@router.put("/close/{task_id}")
def close(task_id: UUID):
    with session_maker() as session:
        task = get_task_row(session, task_id)
            
        if task == None or task.is_cleaned:
            return
        
    try:
        file_name = str(task_id) + '.mp4'
        file_version = b2_bucket.get_file_info_by_name(file_name)
        b2_bucket.delete_file_version(
            file_id=file_version.id_,
            file_name=file_name
        )
    except:
        pass
    
    with session_maker() as session:
        statement = (
            update(ConvertMp4Task)
            .where(ConvertMp4Task.key == task_id)
            .values(is_cleaned=True)
        )
        session.execute(statement)
        session.commit()
            