from worker.main import app
import subprocess
import os
from common.config import settings
from datetime import datetime, timezone, timedelta
import shutil
from sqlalchemy import select, update, and_
from common.data.sqlalchemy.engine import session_maker
from common.data.sqlalchemy.models.convert_to_mp4 import ConvertMp4Task
from common.constants.convert_to_mp4 import PENDING, COMPLETED, FAILED

CONVERT_TO_MP4_DIR = "convert_to_mp4"

def delete_dir(dir_path):
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        shutil.rmtree(dir_path)
        
@app.task(name="convert_to_mp4.convert", bind=True)
def convert(self, video_url: str, file_name: str):
    task_id = self.request.id
    output_dir = os.path.join(settings.shared_files_path, CONVERT_TO_MP4_DIR, task_id)
    output_path = os.path.join(output_dir, file_name)

    try:
        os.makedirs(output_dir, exist_ok=True)
        
        subprocess.run(
            ["ffmpeg", "-loglevel", "error", "-nostdin", "-i", video_url, "-c", "copy", "-bsf:a", "aac_adtstoasc", output_path],
            check=True,
            timeout=settings.ffmpeg_timeout_seconds
        )
    except:
        delete_dir(output_dir)
        
        with session_maker() as session:
            with session.begin():
                statement = (
                    update(ConvertMp4Task)
                    .where(ConvertMp4Task.key == task_id)
                    .values(status=FAILED, is_cleaned=True)
                )
                session.execute(statement)
                session.commit()
        
        raise
    
    with session_maker() as session:
        with session.begin():
            statement = select(ConvertMp4Task).filter_by(key=task_id)
            task = session.scalar(statement)
            
            if task.is_cleaned:
                delete_dir(output_dir)
            
            statement = (
                update(ConvertMp4Task)
                .where(ConvertMp4Task.key == task_id)
                .values(status=COMPLETED)
            )
            session.execute(statement)
            session.commit()

    return output_path

@app.task(name="convert_to_mp4.clean_up_files")
def clean_up_files():
    with session_maker() as session:
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        start = now - timedelta(seconds=settings.result_cleanup_delay_seconds)
    
        statement = select(ConvertMp4Task.key).where(
            and_(
                ConvertMp4Task.is_cleaned == False,
                ConvertMp4Task.updated_at < start
            )
        )
        task_ids = session.scalars(statement).all()
        session.commit()
        
    parent_dir = os.path.join(settings.shared_files_path, CONVERT_TO_MP4_DIR)
    
    for task_id in task_ids:
        delete_dir(os.path.join(parent_dir, str(task_id)))
        
        with session_maker() as session:
            statement = (
                update(ConvertMp4Task)
                .where(ConvertMp4Task.key == task_id)
                .values(is_cleaned=True)
            )
            session.execute(statement)
            session.commit()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(settings.result_cleanup_cycle_seconds, clean_up_files.s())