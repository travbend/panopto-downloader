from main import app
import subprocess
import os
from pathlib import Path
from config import settings

@app.task(name="convert_to_mp4.convert", bind=True)
def convert(self, video_url: str, file_name: str):
    task_id = self.request.id
    output_dir = os.path.join(settings.shared_files_path, task_id)
    output_path = os.path.join(output_dir, file_name)

    os.makedirs(output_dir, exist_ok=True)

    try:
        subprocess.run(
            ["ffmpeg", "-i", "{}".format(video_url), "-c", "copy", "-bsf:a", "aac_adtstoasc", "{}".format(output_path)],
            check=True
        )
    except:
        if os.path.exists(output_path):
            Path.unlink(output_path)
            Path.rmdir(output_dir)

        raise

    return output_path