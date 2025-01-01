from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from uuid import UUID, uuid4
from worker import worker, get_result
import os
from pathlib import Path
import aiofiles

router = APIRouter(
    prefix="/convert-to-mp4",
    tags=["convert-to-mp4"],
    responses={404: {"description": "Not found"}},
)

class InitiateRequest(BaseModel):
    video_url: str
    file_name: str


@router.post("/initiate")
async def initiate(params: InitiateRequest):
    task = worker.send_task('convert_to_mp4.convert', args=[params.video_url, params.file_name])
    return { "task_id": task.id }


@router.get("/status/{task_id}")
async def status(task_id: UUID):
    result = get_result(task_id)
    return result.state

@router.get("/result/{task_id}")
async def result(task_id: UUID, background_tasks: BackgroundTasks):
    result = get_result(task_id)

    if result.state != "SUCCESS":
        raise HTTPException(status_code=400, detail="Task must be successful to download result file")
    
    file_path = result.get()

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404)

    background_tasks.add_task(delete_file, file_path)

    async def file_generator():
        async with aiofiles.open(file_path, mode="rb") as file:
            while chunk := await file.read(1024 * 1024):  # 1MB chunks
                yield chunk

    return StreamingResponse(file_generator(), media_type="application/octet-stream", headers={
        "Content-Disposition": "attachment; filename=large_file.mp4"
    })

    # return FileResponse(file_path, media_type='video/mp4')

def delete_file(file_path):
    if os.path.exists(file_path):
        Path.unlink(file_path)