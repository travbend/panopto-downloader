from worker.main import app
import subprocess
import os
from pathlib import Path
from common.config import settings
from datetime import datetime, timezone, timedelta
from sqlalchemy import select, update, and_
from common.data.sqlalchemy.engine import session_maker
from common.data.sqlalchemy.models.convert_to_mp4 import ConvertMp4Task
from common.data.sqlalchemy.utils import utcnow
from common.constants.convert_to_mp4 import PENDING, COMPLETED, FAILED
from common.data.b2.engine import b2_bucket

CONVERT_TO_MP4_DIR = "convert_to_mp4"
        
@app.task(name="convert_to_mp4.convert", bind=True)
def convert(self, video_url: str):
    task_id = self.request.id
    
    with session_maker() as session:
        statement = (
            update(ConvertMp4Task)
            .where(ConvertMp4Task.key == task_id)
            .values(started_at=utcnow())
        )
        session.execute(statement)
        session.commit()
    
    output_dir = os.path.join(settings.shared_files_path, CONVERT_TO_MP4_DIR)
    output_path = os.path.join(output_dir, task_id + '.mp4')

    try:
        os.makedirs(output_dir, exist_ok=True)
        
        subprocess.run(
            ["ffmpeg", "-loglevel", "error", "-nostdin", "-i", video_url, "-c", "copy", "-bsf:a", "aac_adtstoasc", output_path],
            check=True,
            timeout=settings.ffmpeg_timeout_seconds
        )
        
        b2_bucket.upload_local_file(
            local_file=output_path,
            file_name=task_id + '.mp4'
        )
    except Exception as e:
        with session_maker() as session:
            with session.begin():
                statement = (
                    update(ConvertMp4Task)
                    .where(ConvertMp4Task.key == task_id)
                    .values(status=FAILED, is_cleaned=True, completed_at=utcnow(), error_text=str(e))
                )
                session.execute(statement)
                session.commit()
        
        raise
    finally:
        Path.unlink(output_path)
    
    with session_maker() as session:
        with session.begin():
            statement = (
                update(ConvertMp4Task)
                .where(ConvertMp4Task.key == task_id)
                .values(status=COMPLETED, completed_at=utcnow())
            )
            session.execute(statement)
            session.commit()

@app.task(name="convert_to_mp4.clean_up_files")
def clean_up_files():
    with session_maker() as session:
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        start = now - timedelta(seconds=settings.result_cleanup_delay_seconds)
    
        statement = select(ConvertMp4Task.key).where(
            and_(
                ConvertMp4Task.is_cleaned == False,
                ConvertMp4Task.completed_at.isnot(None),
                ConvertMp4Task.completed_at < start
            )
        )
        task_ids = session.scalars(statement).all()
        session.commit()
        
    parent_dir = os.path.join(settings.shared_files_path, CONVERT_TO_MP4_DIR)
    
    for task_id in task_ids:
        file_path = os.path.join(parent_dir, str(task_id) + '.mp4')
        if os.path.exists(file_path):
            Path.unlink(file_path)
        
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

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(settings.result_cleanup_cycle_seconds, clean_up_files.s().set(priority=10))